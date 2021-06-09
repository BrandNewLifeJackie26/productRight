import styles from './home.css';
import { Button } from 'antd';
import { PieChartTwoTone, ProjectTwoTone } from '@ant-design/icons';

export default function Home() {
    return (
        <div className={styles.container}>
            <div className={styles.welcomeWord}>
                Welcome to The<br/>
                No.1 Professional<br/>
                Analytical Tool<br/>
            </div>
            <div className={styles.intro}>
                <div className={styles.analysisIntro}>
                    <PieChartTwoTone twoToneColor="#0084ff" className={styles.icon}></PieChartTwoTone>
                    <Button type="primary" shape="round" className={styles.buttonLearnMore}>Learn More</Button>
                </div>
                <div className={styles.recommendationIntro}>
                    <ProjectTwoTone twoToneColor="#188fff" className={styles.icon}></ProjectTwoTone>
                    <Button type="primary" shape="round" className={styles.buttonLearnMore}>Learn More</Button>
                </div>
            </div>
        </div>
    );
}