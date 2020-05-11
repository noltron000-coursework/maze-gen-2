import Graph from './graph'
import {GraphType} from './types'
import HypercubeGraph from './graph/hypercube'
import Cell from './cell'

// export those who will never have breaking changes.
export {
	GraphType,
	HypercubeGraph,
	Cell,
}

// export a omnipotent class-generator class.
// this is expiremental, so be on your guard.
export default Graph
