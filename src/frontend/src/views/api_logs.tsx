import React, { useEffect, useState } from 'react';
import { View } from '@/library/types';
import { Router, useNavigate } from '@reach/router';
import { Log, PaginatedLogs, state } from '@/library/api';
import LogList from '@/components/sections/log-list';
import LogDetails from '@/components/sections/log-details';

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

export function formatDate(date_string: string): string {
  const date = new Date(date_string);
  let [month, day, year] = date.toLocaleDateString().split("/");
  let [hour, minute, second] = date.toLocaleTimeString().split(/:| /);
  return `${day}/${month}/${year}, ${hour}:${minute}:${second}`;
}

export default APILogs;