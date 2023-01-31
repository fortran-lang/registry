import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { CookiesProvider } from 'react-cookie';
import { configureStore } from '@reduxjs/toolkit'
import { Provider } from 'react-redux';
import rootReducer from './store/reducers/rootReducer';


const root = ReactDOM.createRoot(document.getElementById('root'));
const store =  configureStore({
  reducer: rootReducer,
})
root.render(
  // <React.StrictMode>import { CookiesProvider } from 'react-cookie';
<Provider store={ store }>
<CookiesProvider><App /></CookiesProvider>
</Provider>    
  // </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
