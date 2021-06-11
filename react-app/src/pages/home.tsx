import styles from './home.css';
import { Tooltip, Button } from 'antd';
import { PieChartTwoTone, ProjectTwoTone } from '@ant-design/icons';
import { Link } from 'react-router-dom';

export default function Home() {
    const recommendationDesc = `
        Explore recommendations on similar items and potential buyers to pitch a target item for 
        increasing overall sales of the organization
    `;
    const analysisDesc = `
        Explore the sales, conversion, and funnel KPIs for your best selling 
        Brands, Categories, and Products
    `;

    return (
        <div className={styles.container}>
            <div className={styles.welcomeWord}>
                Welcome to The<br/>
                No.1 Professional<br/>
                Analytical Tool<br/>
                <i style={{color: "darkblue"}}><b>Product Right</b></i> <br/>
            </div>
            <div className={styles.intro}>
                <div className={styles.analysisIntro}>
                    <Link to="/analysis">
                        <Tooltip title={analysisDesc}>
                            <PieChartTwoTone twoToneColor="#0084ff" className={styles.icon}></PieChartTwoTone>
                        </Tooltip>
                    </Link>
                    <Link to="/analysis">
                        <Button type="primary" shape="round" className={styles.buttonLearnMore}>Analysis Dashboard</Button>
                    </Link>
                </div>
                <div className={styles.recommendationIntro}>
                    <Link to="/recommendation">
                        <Tooltip title={recommendationDesc} color="blue">
                            <ProjectTwoTone twoToneColor="#188fff" className={styles.icon}></ProjectTwoTone>
                        </Tooltip>
                    </Link>
                    <Link to="/recommendation">
                        <Button type="primary" shape="round" className={styles.buttonLearnMore}>Recommendation Engine</Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}