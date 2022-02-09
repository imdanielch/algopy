import { useContext, useRef, useEffect } from "react";
import { select, scaleTime, timeDay, scaleBand, axisBottom } from "d3";
import { ChartContext } from "./_chartcontext";

export const XAxis = ({ xDomain, tickCount }) => {
  const defaultxDomain = [0, 100];
  const defaulttickCount = 10;
  xDomain = xDomain ? xDomain : defaultxDomain;
  tickCount = tickCount ? tickCount : defaulttickCount;
  const prefs = useContext(ChartContext);
  const width = prefs.containerWidth;
  const height = prefs.containerHeight;
  const { left, right, bottom } = prefs.containerMargin;
  const xAxisRef = useRef(null);

  useEffect(() => {
    const x = scaleBand()
      .domain(xDomain)
      .rangeRound([left, width - right]);
    //.padding(prefs.padding);
    const axis = axisBottom;
    const xAxis = axis(x)
      //.ticks(tickCount)
      .tickValues(
        x.domain().filter(function (d, i) {
          return !(i % 5);
        })
      )
      .tickFormat((x) => new Date(x).toLocaleString())
      .tickSizeOuter(0);
    //.tickFormat((x) => new Date(x).toLocaleString())

    select(xAxisRef.current).call(xAxis);
  }, [left, right, tickCount, width, xDomain]);

  return <g transform={`translate(0, ${height - bottom})`} ref={xAxisRef} />;
};
