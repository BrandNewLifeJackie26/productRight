import React, { useEffect } from 'react';
import styles from './analysis.css';
import { useState } from 'react';
import BarChart from '../components/charts/barchart'

export default function Analysis() {
    // Vega object
    const [specTopCategoriesBySales, setSpecTopCategoriesBySales] = useState({});
    const [specCustomerBehaviorByCategory, setSpecCustomerBehaviorByCategory] = useState({});
    const [specTopBrandsByCategory, setSpecTopBrandsByCategory] = useState({});
    const [specTopItemsByCategory, setSpecTopItemsByCategory] = useState({});

    const [specTopBrandsBySales, setSpecTopBrandsBySales] = useState({});
    const [specCustomerBehaviorByBrand, setSpecCustomerBehaviorByBrand] = useState({});
    const [specTopItemsByBrand, setSpecTopItemsByBrand] = useState({});

    const [specDailySalesByCategoryAndBrand, setSpecDailySalesByCategoryAndBrand] = useState({});
    const [specCustomerBehaviorByCategoryAndBrand, setSpecCustomerBehaviorByCategoryAndBrand] = useState({});
    
    // Get vega object
    useEffect(()=>{
      fetch('/api/top-categories-by-sales-with-revenue').then(res => res.json()).then(data => {
        setSpecTopCategoriesBySales(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/customer-behavior-by-category').then(res => res.json()).then(data => {
        setSpecCustomerBehaviorByCategory(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/top-brands-by-sales-with-revenues').then(res => res.json()).then(data => {
        setSpecTopBrandsBySales(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/customer-behavior-by-brand').then(res => res.json()).then(data => {
        setSpecCustomerBehaviorByBrand(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/daily-sales-by-category-and-brand').then(res => res.json()).then(data => {
        setSpecDailySalesByCategoryAndBrand(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/customer-behavior-by-category-and-brand').then(res => res.json()).then(data => {
        setSpecCustomerBehaviorByCategoryAndBrand(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/brands-by-category').then(res => res.json()).then(data => {
        setSpecTopBrandsByCategory(data);
      })
    }, []);

    useEffect(() => {
      fetch('/api/top-items-by-category').then(res => res.json()).then(data => {
        setSpecTopItemsByCategory(data);
      })
    }, []);

    useEffect(() => {
      fetch('/api/top-items-by-brand').then(res => res.json()).then(data => {
        setSpecTopItemsByBrand(data);
      })
    }, []);
  
    return (
      <>
        <div>
        <h1 className={styles.title}>Analysis</h1>
        </div>

        <div>
        <h2 className={styles.subtitle}>Category Level</h2>
        </div>
        <table width='100%'>
          <tbody>
            <tr>
              <td align='center'><BarChart spec={specTopCategoriesBySales}></BarChart></td>
              <td align='center'><BarChart spec={specCustomerBehaviorByCategory}></BarChart></td>
            </tr>
            <tr>
              <td align='center'><BarChart spec={specTopBrandsByCategory}></BarChart></td>
              <td align='center'><BarChart spec={specTopItemsByCategory}></BarChart></td>
            </tr>
          </tbody>
        </table>
        
        <div>
        <h2 className={styles.subtitle}>Brand Level</h2>
        </div>
        <table width='100%'>
          <tbody>
            <tr>
              <td align='center'><BarChart spec={specTopBrandsBySales}></BarChart></td>
              <td align='center'><BarChart spec={specCustomerBehaviorByBrand}></BarChart></td>
            </tr>
            <tr>
              <td align='center'><BarChart spec={specTopItemsByBrand}></BarChart></td>
            </tr>
          </tbody>
        </table>

        <div>
        <h2 className={styles.subtitle}>Daily Level</h2>
        </div>
        <table width='100%'>
          <tbody>
            <td align='center'><BarChart spec={specDailySalesByCategoryAndBrand}></BarChart></td>
          </tbody>
        </table>

        <div>
        <h2 className={styles.subtitle}>Others</h2>
        </div>
        <table width='100%'>
          <tbody>
            <td align='center'><BarChart spec={specCustomerBehaviorByCategoryAndBrand}></BarChart></td>
          </tbody>
        </table>
      </>
    );
  }
  