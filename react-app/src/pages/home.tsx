import styles from './home.css';
import { Layout } from 'antd';

export default function Home() {
    return (
        <div className={styles.welcomeWord}>
            Welcome to Your<br/>
            1st Professional<br/>
            Analytical Tool<br/>
        </div>
    );
}