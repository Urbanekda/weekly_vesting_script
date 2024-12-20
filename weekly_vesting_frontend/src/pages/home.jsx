import React from "react";
import { useState } from 'react'
import KeyPoints from "../components/keyPoints"
import TokenSection from '../components/tokenSection'
import HonorableMentions from '../components/honorableMentions'
import FinalSection from '../components/finalSection'
import Intro from '../components/intro'

export default function Home (){
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null)

  function handleClick() {
    setLoading(true);
    setError(null);

    fetch("http://127.0.0.1:5000/api/scrape/main")
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((result) => {
            setData(result);
            setLoading(false);
          })
          .catch((error) => {
            setError(error.message);
            setLoading(false);
          });
          
  }
    
    return(
        <div>
            <Intro />
            <button onClick={handleClick}>Scrape data</button>
            {loading && (<button>Loading...</button>)}
            {data && (<KeyPoints data={data} />)}

            {data ? (
             data.map((project, index) => (<TokenSection project={project} key={index} />))
            ) : (
             <p>No data available, click button to fetch data.</p>)}
         <HonorableMentions data={data} />
         <FinalSection />
        </div>
    )
}