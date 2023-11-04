import React, { useContext, useEffect, useRef, useState } from 'react';
import { isNoneOrEmpty, useLocation } from '@/lib/helper';
import { useRouter } from 'next/dist/client/router';

interface TabsComponent extends React.HTMLAttributes<HTMLDivElement> {
  eventKey?: string;
  tabClass?: string;
  tabContainerClass?: string;
  onSwitch?: (tab: string) => void;
}
interface TabStateInterface {
  disabledTabs?: string[];
  tabs: string[];
  selected: string;
  selectTab: (tab: string, disabled?: string[] | undefined) => void;
}
interface TabStateProviderProps {
  tabs: string[];
  disabledTabs?: string[];
  defaultSelected?: string;
  setSelectedToURL?: boolean;
}

export const TabStateContext = React.createContext<TabStateInterface>({} as TabStateInterface);

export const TabStateProvider: React.FC<TabStateProviderProps> = ({ children, tabs, defaultSelected, disabledTabs = [], setSelectedToURL }) => {
  const router = useRouter();
  const { tab } = router.query;
  const { addUrlParam } = useLocation();
  const [selected, setSelected] = useState<string>(defaultSelected || tabs[0]);
  const [initialized, setInitialized] = useState<boolean>(false);

  const selectTab = (tab: string, disabled?: string[]) => {
    disabled = disabled || disabledTabs || [];
    if (!tabs.includes(tab)) { return; };
    if (disabled && disabled.includes(tab)) { return; };

    setSelected(tab);
  };

  useEffect(() => { setSelectedToURL && addUrlParam('tab', selected); }, [selected]);
  useEffect(() => {
    if (!initialized && setSelectedToURL && !isNoneOrEmpty(tab) && !(disabledTabs || []).includes(tab as string) && tab !== selected) {
      setSelected(tab as string);
      setInitialized(true);
    }
  }, [tab, disabledTabs])

  return (
    <TabStateContext.Provider value={{
      tabs,
      disabledTabs,
      selected,
      selectTab,
    }}>
      {children}
    </TabStateContext.Provider>
  )
};

const Tabs: React.FC<TabsComponent> = ({ eventKey, tabClass, tabContainerClass, children, onSwitch, ...props }) => {
  const { tabs, disabledTabs, selected, selectTab } = useContext(TabStateContext);
  const ref = useRef<any>();

  const __ = (tab: string) => (_?: any) => { selectTab(tab); };
  ref?.current?.addEventListener((eventKey || 'tab-updated'), (e: CustomEvent<any>) => {
    setTimeout(() => __(e.detail.nextTab)(), e.detail.delay || 0);
  });

  useEffect(() => { onSwitch && onSwitch(selected) }, [selected]);

  return (
    <>

      <div className={`tabs ${tabContainerClass || ''}`}>
        <ul>

          {(tabs || []).map((tab, index) => (
            <li key={index} className={`${tabClass} ${selected === tab ? "is-active" : ""}`}>
              <a onClick={__(tab)} data-name={tab} className={`is-capitalized ${(disabledTabs || []).includes(tab) ? "is-disabled" : ""}`}>
                {tab}
              </a>
            </li>
          ))}

        </ul>
      </div>

      <div {...props} ref={ref}>
        {React.Children.map(children, (child: any, index) => {
          const isActive = tabs && selected === tabs[index];
          return (
            <div key={index} className={`tab-content ${isActive ? "is-active" : ""}`}>
              {child}
            </div>
          );
        })}
      </div>

    </>
  )
};

export default Tabs;
