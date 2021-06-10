import styles from './home.css';
import { Tooltip, Button } from 'antd';
import { PieChartTwoTone, ProjectTwoTone } from '@ant-design/icons';
import { Link } from 'react-router-dom';

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
                    <Link to="/analysis">
                        <Tooltip title="Analysis dashboard">
                            <PieChartTwoTone twoToneColor="#0084ff" className={styles.icon}></PieChartTwoTone>
                        </Tooltip>
                    </Link>
                    <Link to="/analysis">
                        <Button type="primary" shape="round" className={styles.buttonLearnMore}>Learn More</Button>
                    </Link>
                </div>
                <div className={styles.recommendationIntro}>
                    <Link to="/recommendation">
                        <Tooltip title="Recommendation" color="blue">
                            <ProjectTwoTone twoToneColor="#188fff" className={styles.icon}></ProjectTwoTone>
                        </Tooltip>
                    </Link>
                    <Link to="/recommendation">
                        <Button type="primary" shape="round" className={styles.buttonLearnMore}>Learn More</Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}