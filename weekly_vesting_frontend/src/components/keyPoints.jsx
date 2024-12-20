import React, { useEffect, useState } from "react";

export default function KeyPoints({ data }) {  
  const [processedData, setProcessedData] = useState([]);

  useEffect(() => {
    function sumSupplyIncrease(data) {
      const newData = JSON.parse(JSON.stringify(data));

      newData.forEach(project => {
        let totalSupplyIncrease = 0;

        project.forEach(group => {
          const increase = parseFloat(group.supplyIncrease.replace('%', ''));
          if (!isNaN(increase)) {
            totalSupplyIncrease += increase;
          }
        });

        totalSupplyIncrease = totalSupplyIncrease.toFixed(2) + "%";

        project[0].totalSupplyIncrease = totalSupplyIncrease;
      });

      return newData;
    }

    const updatedData = sumSupplyIncrease(data);
    setProcessedData(updatedData);
  }, [data]);

  return (
    <div>
      <h2>🔒 Interesting Token Unlocks This Week:</h2>
      <ul>
        {processedData.map((project, index) => (
          <li key={index}>
            <a href={project[0].link}>{project[0].ticker}</a> - 
            <strong> {project[0].totalSupplyIncrease} of the total supply</strong> will enter circulation on 
            <strong> {project[0].unlockDate}.</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}
