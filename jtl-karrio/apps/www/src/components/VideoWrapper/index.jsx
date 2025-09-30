import React from "react";

import styles from "./styles.module.css";

const VideoWrapper = ({ children }) => (
  <div class={styles.videoWrapper}>
    {children}
  </div>
);

export default VideoWrapper;
