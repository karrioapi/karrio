"use client";

import * as React from "react";
import { cn } from "@karrio/ui/lib/utils";
import { formatDayDate, isNone } from "@karrio/lib";

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
}

interface RecentActivityProps {
  tracker: TrackerData | null;
  className?: string;
}

const getActivityIcon = (description: string | null, delivered?: boolean | null) => {
  if (delivered) {
    return <i className="fas fa-check-circle text-green-600" />;
  }

  const desc = description?.toLowerCase() || '';

  if (desc.includes('delivered')) {
    return <i className="fas fa-check-circle text-green-600" />;
  }
  if (desc.includes('out for delivery')) {
    return <i className="fas fa-truck text-blue-600" />;
  }
  if (desc.includes('in transit') || desc.includes('departed') || desc.includes('left')) {
    return <i className="fas fa-shipping-fast text-blue-600" />;
  }
  if (desc.includes('picked up') || desc.includes('pickup')) {
    return <i className="fas fa-hand-holding text-orange-600" />;
  }
  if (desc.includes('arrived') || desc.includes('arrival')) {
    return <i className="fas fa-plane-arrival text-blue-600" />;
  }

  return <i className="fas fa-circle text-gray-400" />;
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

  return (
    <div className={cn("space-y-4", className)}>
      {activities.length === 0 ? (
        <div className="text-sm text-gray-500">
          No recent activity to display
        </div>
      ) : (
        <>
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-start gap-3">
              {/* Activity Icon */}
              <div className="flex-shrink-0 mt-0.5 text-xs">
                {getActivityIcon(activity.description, activity.isDelivered)}
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
          ))}
        </>
      )}
    </div>
  );
};