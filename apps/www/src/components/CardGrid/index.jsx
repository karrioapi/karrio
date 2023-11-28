import React from "react";

import styles from "./styles.module.css";

const CardGrid = ({ children, home = false }) => (
  <section className={"row " + styles.cardGrid}>
    {"map" in children ? (
      children.map((child) => (
        <article className="col col--6 my-5">{child}</article>
      ))
    ) : (
      <article className="col col--6 my-5">{children}</article>
    )}
  </section>
);

export default CardGrid;
