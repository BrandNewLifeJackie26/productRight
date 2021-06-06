import styles from './index.less';
import { Layout, Menu } from 'antd';
import React, { useEffect, useState } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom';
import CustomizedMenu from '../components/menu/menu';
import Home from './home';
import Analysis from './analysis';
import Recommendation from './recommendation';

import Logo from '../assets/logo.png'

const { Header, Content, Footer, Sider } = Layout;

export default function IndexPage() {
  // Get time
  const [currentTime, setCurrentTime] = useState(0);

  // Set collapsed
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    // Set current time
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  // Return layout
  return (
    <Router>
      <Layout className={styles.layout}>
        <Sider collapsible collapsed={collapsed} onCollapse={collapsed => setCollapsed(collapsed)}>
          <img src={Logo} className={styles.logo}></img>
          <CustomizedMenu/>
        </Sider>

        <Layout className={styles.contentBackground}>
          <Header className={styles.header}>YOUR BEST FRIEND: PRODUCT RIGHT!</Header>
          
          <Content className={styles.content}>
            <Switch>
              <Route path='/recommendation'>
                <Recommendation></Recommendation>
              </Route>
              
              <Route path='/analysis'>
                <Analysis></Analysis>
              </Route>

              <Route path='/'>
                <Home></Home>
              </Route>
            </Switch>
          </Content>
        </Layout>

      </Layout>
    </Router>
  );
}
