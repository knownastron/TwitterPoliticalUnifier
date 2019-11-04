import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';
// reducer (function), preloaded state (if any), enhancer (function)

const initialState = {};

const middleware = [thunk]; // thunk allows direct calls to dispatch function for async requests

const store = createStore(
  rootReducer,
  initialState,
  applyMiddleware(...middleware)
);

export default store;
