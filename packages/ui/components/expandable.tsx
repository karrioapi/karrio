import React from "react";

interface ExpandableComponent {
  className?: string;
  children?: React.ReactNode;
}

export const Expandable = ({
  className,
  children,
}: ExpandableComponent): JSX.Element => {
  const [isExpanded, setIsExpanded] = React.useState(false);

  return (
    <div
      className={className ? className : ""}
      style={
        isExpanded
          ? { position: "relative" }
          : { position: "relative", maxHeight: "35vh", overflow: "hidden" }
      }
    >
      {children}

      <div
        className="is-flex is-justify-content-center"
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          left: 0,
          backgroundImage:
            "linear-gradient(to bottom, rgba(255,0,0,0), rgba(255,255,255,1))",
        }}
      >
        <button
          className="button is-small is-default"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <span>{isExpanded ? "minimize lines" : "expand lines"}</span>
          <span className="icon is-small">
            <i
              className={`fas ${isExpanded ? "fa-chevron-up" : "fa-chevron-down"}`}
            ></i>
          </span>
        </button>
      </div>
    </div>
  );
};
