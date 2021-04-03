import React from 'react';
import { View } from '@/library/types';
import { Router } from '@reach/router';
import LogList from '@/components/sections/log-list';
import LogDetails from '@/components/sections/log-details';
import LogsQuery from '@/components/data/logs-query';
import LogQuery from '@/components/data/log-query';

interface APILogsView extends View { }

const APILogPage: React.FC<APILogsView> = () => {

  return (
    <LogsQuery>
      <LogQuery>
        <Router>
          <LogList path="/" />
          <LogDetails path="/:logId" />
        </Router>
      </LogQuery>
    </LogsQuery>
  );
}

export default APILogPage;