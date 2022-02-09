import { useContext, useRef, useEffect } from "react";
import { select, scaleLinear, axisLeft } from "d3";
import { ChartContext } from "./_chartcontext";

export const YAxis = ({ yDomain, tickCount }) => {
  const defaultyDomain = [0, 100];
  const defaulttickCount = 10;
  yDomain = yDomain ? yDomain : defaultyDomain;
  tickCount = tickCount ? tickCount : defaulttickCount;
  const prefs = useContext(ChartContext);
  const width = prefs.containerWidth;
  const height = prefs.containerHeight;
  const { left, top, bottom } = prefs.containerMargin;
  const yAxisRef = useRef(null);

  useEffect(() => {
    const y = scaleLinear()
      .domain(yDomain)
      .range([height - bottom, top]);
    const axis = axisLeft;
    const yAxis = axis(y).ticks(tickCount).tickSizeOuter(0);

    select(yAxisRef.current).call(yAxis);
  }, [left, top, bottom, tickCount, height, yDomain]);

  return <g transform={`translate(${left}, 0)`} ref={yAxisRef} />;
};
