import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

export default function Heading({title}) {

	const [ _title, setTitle ] = useState(title)
  const [ clicked, setClicked] = useState(false)

	function onChangeHandler(event) {
		setTitle(event.target.value)
	}

	const isMounted = useRef(false)

	// add a delay, then execute the api call on cleanup
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
			  POST()
			} else {
					isMounted.current = true
				}
    }, 1500)
		return( () => clearTimeout(delayDebounceFn) )
  }, [_title])


	const POST = () => {
		fetch(CONTEXT.edit_tearsheet_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: JSON.stringify({'data': {'title': _title }
			 }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
	}

	return (
		<div className="text-gray-500 text-left">
			<a className="text-xs" href={CONTEXT.view_tearsheet}> {'<<< detail'}</a>
			{ clicked ?
				<input onChange={ (event) => onChangeHandler(event)} style={{'font-size': '30px'}} className="py-2 text-gray-500 text-left" value={_title}></input> : <span onClick={ ()=> { setClicked(true)}}  style={{'width': '300px', 'display': 'block', 'font-size': '30px'}} className="py-2 text-gray-500 text-left">{_title}</span>
			}
		</div>
	)
}
