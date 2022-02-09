import { useEffect, useState } from "react";
import Chart from "./chart";
import styles from "../../styles/Sample.module.css";

function Sample({ data }) {
  const [entries, setEntries] = useState([]);
  useEffect(() => {
    setEntries(data);
  }, [data]);
  return (
    <div className={styles.App}>
      <Chart data={entries} height={500} width={1000} />
      <br />
      {
        "http://localhost:3000/charts/sample?symbol={symbol}&sd={start_datetime}&ed={end_datetime}&res={res}"
      }
      <br />
      ISO 8601 datetime format: e.g. 2022-01-01T08:45:00
    </div>
  );
}

export async function getServerSideProps(context) {
  const { symbol, sd, ed, res } = context.query;
  console.log(context.query);
  const url = `http://localhost:8000/symbol/${symbol}/${sd}/${ed}/${res}`;
  const response = await fetch(url);
  const data = await response.json();
  return {
    props: { data }, // will be passed to the page component as props
  };
}

export default Sample;
