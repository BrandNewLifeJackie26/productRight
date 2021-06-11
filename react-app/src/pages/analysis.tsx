import React, { useEffect, useState } from 'react';
import { Button, Carousel, Timeline } from 'antd';
import {
  LeftCircleFilled,
  RightCircleFilled
} from '@ant-design/icons';

import styles from './analysis.css';
import BarChart from '../components/charts/barchart'

/* Arrows used in carousel */
function PrevArrow(props) {
  const { className, style, onClick } = props;
  return (
    <LeftCircleFilled
      className={styles.carouselPrevArrow}
      onClick={onClick}
    />
  );
}

function NextArrow(props) {
  const { className, style, onClick } = props;
  return (
    <RightCircleFilled
      className={styles.carouselNextArrow}
      onClick={onClick}
    />
  );
}

/* Generate charts */
function Charts(props) {
  const charts = props.levelMap[props.level].map((item) => (
    <div className={styles.carouselItem}>
      <BarChart spec={item["spec"]}></BarChart>
    </div>
  ));
  return (
    <Carousel
      ref={props.refCarousel}
      className={styles.carousel}
      arrows={true}
      prevArrow={<PrevArrow />}
      nextArrow={<NextArrow />}
      afterChange={(current) => {props.onAfterChange(current)}}
      >              
      {charts}
    </Carousel>
  );
}

/* Generate descriptions */
function Descriptions(props) {
  const descriptions = props.levelMap[props.level].map((item, index) => (
    index == props.highlightedIndex ?
    <Timeline.Item className={styles.analysisIntroItem} style={{color: "black", fontWeight: "bold"}}>{item["desc"]}</Timeline.Item> :
    <Timeline.Item className={styles.analysisIntroItem}><text id={`desc-${index}`} onClick={(val) => props.onClickDescId(val.target.id)}>{item["desc"]}</text></Timeline.Item>
  ));
  return (
    <div className={styles.analysisIntro}>
      <div className={styles.analysisIntroTitle}>{props.level}</div>
      <Timeline className={styles.analysisIntroBody}>{descriptions}</Timeline>
    </div>
  );
}

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
    
    // Map of levels
    const levelMap = {
      "Category": [
        {"spec": specTopCategoriesBySales, "desc": "Click to see the top categories and the number of products that each category sold"},
        {"spec": specCustomerBehaviorByCategory, "desc": "Select a category from the drop down box to see the number of customers who viewed the category, added a product in the category to the cart, and bought a product in the category"},
        {"spec": specTopBrandsByCategory, "desc": "Select a category from the drop down box to see its top brands based on the number of products sold"},
        {"spec": specTopItemsByCategory, "desc": "Select a category from the drop down box to see its top selling items"}
      ],
      "Brand": [
        {"spec": specTopBrandsBySales, "desc": "Click to see the top brands and the number of products that each brand sold"},
        {"spec": specCustomerBehaviorByBrand, "desc": "Select a brand from the drop down box to see the number of customers who viewed a product from the brand, added a product from the brand to the cart, and bought a product from the brand"},
        {"spec": specTopItemsByBrand, "desc": " Select a brand from the drop down box to see its top selling items"}
      ],
      "Daily": [
        {"spec": specDailySalesByCategoryAndBrand, "desc": "Select a category and a brand in the drop down box to the see the number of products that were sold from the brand daily"}
      ],
      "Others": [
        {"spec": specCustomerBehaviorByCategoryAndBrand, "desc": "Select a category and a brand from the drop down box to see the number of customers who viewed a product from this brand in this category, added those products and bought them"}
      ],
    }

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

    // Selected analysis level
    const [analysisLevel, setAnalysisLevel] = useState("Category");

    // Selected page
    const [carouselIndex, setCarouselIndex] = useState(0);

    // Carousel reference
    const refCarousel = React.createRef();

    return (
      <>
        <div className={styles.levelSelection}>
          <div className={styles.selectionIntro}>Click Level to Analyze</div>
          <div className={styles.selections}>
            <Button type="primary" shape="round" className={styles.selectionButton} onClick={() => setAnalysisLevel("Category")} autoFocus={true}>Category</Button>
            <Button type="primary" shape="round" className={styles.selectionButton} onClick={() => setAnalysisLevel("Brand")}>Brand</Button>
            <Button type="primary" shape="round" className={styles.selectionButton} onClick={() => setAnalysisLevel("Daily")}>Daily</Button>
            <Button type="primary" shape="round" className={styles.selectionButton} onClick={() => setAnalysisLevel("Others")}>Others</Button>
          </div>
        </div>

        <div className={styles.analysis}>
          <Descriptions 
            level={analysisLevel} 
            levelMap={levelMap} 
            highlightedIndex={carouselIndex} 
            onClickDescId={(descIdString) => {
              let strArr = descIdString.split('-');
              if (refCarousel != null) {
                refCarousel.current.goTo(parseInt(strArr[strArr.length-1]));
              }
            }}
          />
          <div className={styles.analysisChart}>
            <Charts
              level={analysisLevel}
              levelMap={levelMap}
              refCarousel={refCarousel}
              onAfterChange={(current) =>{
                setCarouselIndex(current)
              }}
            />            
          </div>
        </div>
      </>
    );
  }
  