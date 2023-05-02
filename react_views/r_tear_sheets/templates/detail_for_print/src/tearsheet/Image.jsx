import { useState, useRef, useEffect } from 'react';

export default function Image({img }) {

	return (
		<div>
				<img className='object-fill' src={img}/>
		</div>
	)
}
