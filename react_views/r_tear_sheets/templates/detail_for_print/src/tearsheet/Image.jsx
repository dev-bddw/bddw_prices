import { useState, useRef, useEffect } from 'react';

export default function Image({img }) {

	return (
		<div>
				<div className="relative">
					<img style={{'width': '850px'}} className='object-fill' src={img}/>
				</div>
		</div>
	)
}
