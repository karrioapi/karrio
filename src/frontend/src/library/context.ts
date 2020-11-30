import { References } from '@purplship/purplship';
import React from 'react';
import { PaginatedLogs, UserInfo } from '@/library/api';

export const Reference = React.createContext<References>({} as References);
export const Logs = React.createContext<PaginatedLogs>({} as PaginatedLogs);
export const User = React.createContext<UserInfo>({} as UserInfo);
