import { References } from '@purplship/purplship';
import React from 'react';
import { PaginatedLogs } from '@/library/api';

export const Reference = React.createContext<References>({} as References);
export const Logs = React.createContext<PaginatedLogs>({} as PaginatedLogs);
