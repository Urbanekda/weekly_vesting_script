import React from "react";

export default function TokenSection({ project }){
    
    return (
        <div>
            <h2>{project[0].name} - {project[0].ticker} Token Unlock</h2>
            <p>Token description</p>
            <div>
                <iframe width="100%" height="372" frameBorder="0" scrolling="no" src={project[0].link + "/ticker?theme=light&padding=16&type=large&currency=USD&blocks=price%2CmarketCap%2Cvolume24h%2Cliquidity"}></iframe>
                <p>On <strong>{project[0].unlockDate} {project[0].name}</strong> is set for the following unlocks:</p>
                <ul>
                    {project.map((group, index) => (<li key={index}><strong>{group.amount} {group.ticker}</strong> tokens valued at <strong>{group.valuation}</strong> will be released to the "<strong>{group.allocationGroup}</strong>" allocation group, increasing the circulating supply by <strong>{group.supplyIncrease}</strong></li>))}
                </ul>
            </div>
        </div>
    );
};