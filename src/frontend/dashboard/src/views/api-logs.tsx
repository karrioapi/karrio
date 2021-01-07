import React, { useEffect, useState } from 'react';
import { Log, PaginatedLogs, View } from '@/library/types';
import { Router, useNavigate } from '@reach/router';
import LogList from '@/components/sections/log-list';
import LogDetails from '@/components/sections/log-details';
import { state } from '@/library/api';

interface APILogsView extends View {
  logs?: PaginatedLogs;
}

const APILogs: React.FC<APILogsView> = ({ logs }) => {
  useEffect(() => { if(logs === undefined ) state.fetchLogs(); }, []);
  const [log, setLog] = useState<Log>();
  const navigate = useNavigate();
  const handleLogSelection = (log: Log) => (_: any) => {
    navigate(`api_logs/${log.id}`);
    setLog(log);
  };

  return (
    <Router>
      <LogList path="/" logs={logs} handleLogSelection={handleLogSelection}/>
      <LogDetails path="/:logId" logs={logs} log={log} setLog={setLog}/>
    </Router>
  );
}

export default APILogs;