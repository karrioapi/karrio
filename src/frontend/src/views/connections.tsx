import React, { Fragment, useContext } from 'react';
import { View } from '@/library/types';
import ConnectProviderModal from '@/components/connect-provider-modal';
import Tabs from '@/components/generic/tabs';
import UserConnectionList from '@/components/sections/user-carrier-list';
import SystemConnectionList from '@/components/sections/system-carrier-list';
import { UserConnections } from '@/components/data/user-connections-query';

interface ConnectionsView extends View {}

const ConnectionsPage: React.FC<ConnectionsView> = ( ) => {
  const { refetch } = useContext(UserConnections);
  const update = async (_?: React.MouseEvent) => refetch && await refetch();

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Carriers</span>
        <ConnectProviderModal className="button is-success is-pulled-right" onUpdate={update}>
          <span>Connect a Carrier</span>
        </ConnectProviderModal>
      </header>

      <div className="table-container">

        <Tabs tabs={['System Connections', 'Your Connections']}>

          <SystemConnectionList />

          <UserConnectionList />

        </Tabs>

      </div>

    </Fragment>
  );
}

export default ConnectionsPage;