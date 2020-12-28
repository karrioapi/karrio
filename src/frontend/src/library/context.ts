import { References } from '@purplship/purplship';
import React from 'react';
import { DefaultTemplates, PaginatedLogs, PaginatedTemplates, UserInfo } from '@/library/types';

export const Reference = React.createContext<References>({} as References);
export const Logs = React.createContext<PaginatedLogs>({} as PaginatedLogs);
export const User = React.createContext<UserInfo>({} as UserInfo);
