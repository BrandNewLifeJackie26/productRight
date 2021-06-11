import styles from './menu.css'

import {
    HomeOutlined,
    BarChartOutlined,
    FundOutlined
} from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { Menu } from 'antd';

export default function CustomizedMenu() {
    return (
        <Menu theme='dark' defaultSelectedKeys={['1']} mode='inline'>
            <Menu.Item key='1' icon={<HomeOutlined className={styles.menuIcon}/>} className={styles.menuItem}>
                <Link to='/'>Home</Link>
            </Menu.Item>
            
            <Menu.Item key='2' icon={<BarChartOutlined className={styles.menuIcon}/>} className={styles.menuItem}>
                <Link to='/analysis'>Analysis</Link>
            </Menu.Item>
            
            <Menu.Item key='3' icon={<FundOutlined className={styles.menuIcon}/>} className={styles.menuItem}>
                <Link to='/recommendation'>Recommendation</Link>
            </Menu.Item>
        </Menu>
    );
}


// export default {
//     title: 'ProductRight',
//     logo: 'https://raw.githubusercontent.com/BrandNewLifeJackie26/productRight/dev/placeholder.png',

//     menuItemRender: (item, dom) => (
//         <>
//             <Link to={item.path}>
//                 <Menu.Item style={{color: 'white', font: 'bold 15px arial,serif'}}>
//                     {dom}
//                 </Menu.Item>
//             </Link>
//         </>
//     ),

//     route: {
//         path: '/menu',

//         routes: [
//             {
//                 path: '/',
//                 name: 'Home',
//                 icon: <HomeOutlined />,
//                 component: './',
//             },
//             {
//                 path: '/analysis',
//                 name: 'Analysis',
//                 icon: <BarChartOutlined />,
//                 component: './analysis',
//             },
//             {
//                 path: '/recommendation',
//                 name: 'Recommendation',
//                 icon: <FundOutlined />,
//                 component: './recommendation',
//             },
//         ],
//     },

//     location: {
//         pathname: '/',
//     },
// };