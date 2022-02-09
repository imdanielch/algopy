import { useState, useRef, useContext, useEffect } from "react";
import * as d3 from "d3";
import { ToolTipContext } from "./_tooltipcontext";

const drawBox = (x, y, width, height) => {
  return `
    M ${x},${y}
    L ${x},${y + height}
    L ${x + width},${y + height}
    L ${x + width},${y}
    L ${x},${y}
    Z
    `;
};

const drawShadow = (start, end, x, width) => {
  return `
    M ${x + width / 2}, ${start}
    V ${end}
    Z
    `;
};

export const CandleStick = (props) => {
  const { TTData, updateTTData } = useContext(ToolTipContext);
  const [stateData, setStateData] = useState(null);
  const [hoverState, setHoverState] = useState(false);

  const csRef = useRef(null);
  const {
    yo,
    yh,
    yl,
    yc,
    y,
    x,
    width,
    height,
    containerWidth,
    containerHeight,
    marginTop,
    marginBottom,
    isLong,
  } = props.data;
  const longc = "#f55";
  const shortc = "#aaa";
  const strokeColor = "#222";
  const color = isLong ? longc : shortc;
  let shadow;

  if (isLong) {
    // Long
    shadow = (
      <>
        <path d={drawShadow(y, yh, x, width)} fill="none" />
        <path d={drawShadow(y + height, yl, x, width)} fill="none" />
      </>
    );
  } else {
    // Short
    shadow = (
      <>
        <path d={drawShadow(y, yh, x, width)} fill="none" />
        <path d={drawShadow(y + height, yl, x, width)} fill="none" />
      </>
    );
  }
  if (yo == yc) {
    color = "black";
  }

  useEffect(() => {
    setStateData(props.tt);
  }, [props.tt]);

  const handleMouseEnter = () => {
    updateTTData(stateData);
    setHoverState(true);
  };

  return (
    <g
      onMouseEnter={handleMouseEnter}
      onMouseLeave={() => setHoverState(false)}
      ref={csRef}
      className="candlestick"
      stroke={strokeColor}
      fill={color}
      strokeWidth="2"
    >
      <path
        fill={hoverState ? "#DDD" : "white"}
        stroke={hoverState ? "#DDD" : "white"}
        d={drawBox(
          x,
          marginTop,
          width,
          containerHeight - marginBottom - marginTop
        )}
      />
      <path d={drawBox(x, y, width, height)} />
      {shadow}
    </g>
  );
};
