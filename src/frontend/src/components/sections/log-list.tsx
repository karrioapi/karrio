import React, { useContext, useEffect } from 'react';
import { LogType, View } from '@/library/types';
import StatusCode from '@/components/status-code-badge';
import { formatDateTime, isNone } from '@/library/helper';
import { Logs } from '@/components/data/logs-query';
import { useNavigate } from '@reach/router';
import { Log } from '@/components/data/log-query';
import { Loading } from '@/components/loader';

interface LogListView extends View {}

const LogList: React.FC<LogListView> = () => {
    const navigate = useNavigate();
    const { setLog } = useContext(Log);
    const { setLoading } = useContext(Loading);
    const { loading, logs, next, previous, load, loadMore } = useContext(Logs);

    const selectLog = (log: LogType) => (_: any) => {
        setLog(log);
        navigate(`api_logs/${log.id}`);
    };

    useEffect(() => { !loading && load() }, []);
    useEffect(() => { setLoading(loading); });

    return (
        <>

            <header className="px-2 pt-1 pb-6">
                <span className="subtitle is-4">API Logs</span>
            </header>

            <div className="table-container">
                <table className="table is-fullwidth is-hoverable is-size-7">

                    <thead className="logs-table">
                        <tr>
                            <th className="status"><span className="ml-2">STATUS</span></th>
                            <th className="description">DESCRIPTION</th>
                            <th className="date has-text-right"><span className="mr-2">DATE</span></th>
                        </tr>
                    </thead>

                    <tbody>
                        {logs.map((log) => (

                            <tr key={log.id} onClick={selectLog(log)}>
                                <td className="status"><StatusCode code={log.status_code as number} /></td>
                                <td className="description">{`${log.method} ${log.path}`}</td>
                                <td className="date has-text-right">
                                    <span className="mr-2">{formatDateTime(log.requested_at)}</span>
                                </td>
                            </tr>

                        ))}
                    </tbody>

                </table>
            </div>


            {(logs.length == 0) && <div className="card my-6">

                <div className="card-content has-text-centered">
                    <p>No API logs has been captured yet.</p>
                    <p>Use the <strong>API</strong> to communicate with your logistic providers.</p>
                </div>

            </div>}

            <footer className="px-2 py-2 is-vcentered">
                <div className="buttons is-centered has-addons">
                    <button className="button is-small" onClick={() => loadMore(previous)} disabled={isNone(previous)}>
                        Previous
                    </button>
                    <button className="button is-small" onClick={() => loadMore(next)} disabled={isNone(next)}>
                        Next
                    </button>
                </div>
            </footer>

        </>
    );
}

export default LogList;
