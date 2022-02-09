import React, { useEffect } from "react";
import styles from "../../styles/Chart.module.css";

export function ToolTip(props) {
  let style;
  if (props.data != null) {
    style = { display: "block", width: props.width };
  } else {
    style = { display: "none" };
  }

  return (
    <div id="tooltip" style={style} className={styles.tooltip}>
      {props.data != undefined
        ? Object.keys(props.data).map((key, index) => (
            <React.Fragment key={index}>
              <span
                style={{
                  paddingLeft: "10px",
                  paddingRight: "4px",
                  fontWeight: "bold",
                  textTransform: "uppercase",
                }}
              >
                {key + ":"}
              </span>
              <span style={{ width: "250px" }}>
                {key == "datetime"
                  ? new Date(props.data[key]).toString()
                  : props.data[key]}
              </span>
            </React.Fragment>
          ))
        : null}
    </div>
  );
}
