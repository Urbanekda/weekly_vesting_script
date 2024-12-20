import React from "react";

export default function VestingTweet ({project}) {
    return (
        <div>
            <p>🔔Unlock reminder: </p>
            <p>Today, {project[0].name} will unlock over VALUATION worth of TICKER tokens to GROUPS vesting groups.</p>
            <p>📈Circulating supply will increase by SUPPLYINCREASE</p>
            <p>#TokenUnlocks #altcoinseason #cryptonewstoday</p>
        </div>
        
    )
}