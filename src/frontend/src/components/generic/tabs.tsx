import React, { useRef, useState } from 'react';

interface TabsComponent extends React.HTMLAttributes<HTMLDivElement> {
    tabs: string[];
    disabled: string[];
    eventKey: string;
    tabClass?: string;
}

const Tabs: React.FC<TabsComponent> = ({ tabs, disabled, eventKey, tabClass, children, ...props }) => {
    const [selected, setSelected] = useState<string>(tabs[0]);
    const ref = useRef<any>();
    const __ = (tab: string) => (_?: any) => {
        setSelected(tab);
    };
    ref?.current?.addEventListener(eventKey, (e: CustomEvent<any>) => {
        setTimeout(() => __(e.detail.nextTab)(), e.detail.delay || 0);
    });

    return (
        <>

            <div className={`tabs ${tabClass}`}>
                <ul>

                    {tabs.map((tab, index) => (
                        <li key={index} className={`${selected === tab ? "is-active" : ""}`}>
                            <a onClick={__(tab)} data-name={tab} className={`is-capitalized ${disabled.includes(tab) ? "is-disabled" : ""}`}>
                                {tab}
                            </a>
                        </li>
                    ))}

                </ul>
            </div>

            <div {...props} ref={ref}>
                {React.Children.map(children, (child: any, index) => {
                    const isActive = selected === tabs[index];
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