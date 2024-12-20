import './App.css'
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import TweetPage from './pages/tweet_page'
import Home from './pages/home';



function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/x" Component={TweetPage} />
          <Route path="/" Component={Home} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
