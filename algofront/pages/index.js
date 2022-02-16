import Head from "next/head";
import Image from "next/image";
import Link from 'next/link'
import styles from "../styles/Home.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="custom charts for Taiwan Futures created by Daniel Chen" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Taiwan Futures Exchange (Taifex) charts
        </h1>

        <p className={styles.description}>
          Source files available on <a href="https://github.com/imdanielch/algopy">GitHub</a>
        </p>

        <div className={styles.grid}>
          <Link href="/charts/sample?symbol=TX&sd=2022-01-04T08:55:00&ed=2022-01-05T12:20:00&res=hour" className={styles.card}>
            <h2>Symbol Charts</h2>
            <p>Simple chart for specific symbol with start datetime and end datetime with a resolution</p>
          </Link>
        </div>
      </main>

    </div>
  );
}
