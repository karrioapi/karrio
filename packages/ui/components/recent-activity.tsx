"use client";

import * as React from "react";
import { cn } from "@karrio/ui/lib/utils";
import { formatDayDate, isNone } from "@karrio/lib";
import { TrackerStatusEnum } from "@karrio/types";

interface TrackingEvent {
  description: string | null;
  location: string | null;
  code: string | null;
  date: string | null;
  time: string | null;
}

interface TrackerData {
  events: TrackingEvent[];
  estimated_delivery?: string | null;
  delivered?: boolean | null;
  status?: TrackerStatusEnum;
}

interface RecentActivityProps {
  tracker: TrackerData | null;
  className?: string;
}

const getActivityIcon = (status?: TrackerStatusEnum, delivered?: boolean | null) => {
  // Green for delivered, gray for everything else
  if (delivered) {
    return <i className="fas fa-circle text-green-600 text-xs" />;
  }

  // Gray for all other cases
  return <i className="fas fa-circle text-gray-400 text-xs" />;
};

export const RecentActivity: React.FC<RecentActivityProps> = ({
  tracker,
  className,
}) => {
  const events = tracker?.events || [];

  // Create activity items from tracking data
  const activities: Array<{
    id: string;
    description: string;
    date: string | null;
    time?: string | null;
    location?: string | null;
    isDelivered?: boolean | null;
  }> = [];

  // Add estimated delivery as first item if available
  if (!isNone(tracker?.estimated_delivery)) {
    activities.push({
      id: 'estimated-delivery',
      description: tracker?.delivered ? 'Package delivered' : 'Estimated delivery',
      date: tracker?.estimated_delivery || null,
      isDelivered: tracker?.delivered
    });
  }

  // Add tracking events
  events.forEach((event, index) => {
    if (event.description) {
      activities.push({
        id: `event-${index}`,
        description: event.description,
        date: event.date,
        time: event.time,
        location: event.location
      });
    }
  });

  // Limit to 2 most recent events
  const recentActivities = activities.slice(0, 2);

  return (
    <div className={cn("space-y-4", className)}>
      {recentActivities.length === 0 ? (
        <div className="text-sm text-gray-500">
          No recent activity to display
        </div>
      ) : (
        <>
          {recentActivities.map((activity, index) => (
            <div key={activity.id}>
              <div className="flex items-start gap-3">
                {/* Activity Icon */}
                <div className="flex-shrink-0">
                  {getActivityIcon(tracker?.status, activity.isDelivered)}
                </div>

                {/* Activity Content */}
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-gray-900">
                    {activity.description}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {activity.date ? formatDayDate(activity.date) : 'Date not available'}
                    {activity.time && `, ${activity.time}`}
                  </div>
                  {activity.location && (
                    <div className="text-xs text-gray-500 mt-1">
                      {activity.location}
                    </div>
                  )}
                </div>
              </div>

              {/* Connecting Line */}
              {index < recentActivities.length - 1 && (
                <div className="flex -my-2">
                  <div className="w-6 flex justify-start pl-1">
                    <div className="w-px h-8 bg-gray-300"></div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </>
      )}
    </div>
  );
};