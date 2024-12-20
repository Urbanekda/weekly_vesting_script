import React from "react";
import VestingTweet from "../components/vesting_tweet";

export default function TweetPage ({data}) {
    return(
        <div>
            {data ? (
            data.map((project, index) => (<VestingTweet project={project} key={index} />))
            ) : (
            <p>No data available.</p>)}
        </div>
    )
}