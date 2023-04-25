import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

export default function Title({title}) {

	return (
		<div className="">
			<div className="py-2 text-gray-500 text-left">
				<span style={{'display': 'block','font-size': '30px'}} >{title}</span>
			</div>
		</div>
	)
}
