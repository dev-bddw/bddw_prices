import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

function Captions({showCreateInputs, captions, sdata}) {

	return(

		<>
			<div style={{'height': sdata.pt_cap}}/>
		<table style={{'width': '850px'}} className="py-5 mx-auto table-auto">
							<thead className="text-gray-400 text-left">
									<th></th>
									<th></th>
									<th></th>
									<th></th>
									<th></th>
							</thead>
							<tbody>
								{ captions.map( (caption, index) => {
									return(<Caption sdata={sdata} caption={caption} index={index}/>)})}
								{ showCreateInputs ?  <AddCaption sdata={sdata}/> : null }
							</tbody>
						</table>
		</>
	)
}

export default Captions;

function AddCaption({sdata}) {

  const [_caption, setCaption] = useState('CAPTION NAME')
	const [_title, setTitle] = useState('CAPTION')
	const [_id, setId] = useState('')

	const CREATE = () => {
		fetch(CONTEXT.create_caption_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: JSON.stringify({'data':{
				'tear_sheet_id': CONTEXT.tearsheet.id,
				'caption_title': _title,
				'caption': _caption
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
		window.location.reload()
		//TODO: api returns new caption ID, then update the list of captions with the new caption values
	}

	function onChangeHandler(event, setter) {
			setter(event.target.value)
	}


	const classes="appearance-none border rounded w-200  py-1 text-gray-400 leading-tight focus:outline-none focus:shadow-outliney-1 w-full"

	return(
			<>
				<tr className="hover:bg-gray-50 text-gray-400 text-left">
						<td style={{'width':`${sdata.d_col_1}px`}}>
							<input onChange={ (event) => onChangeHandler(event, setTitle)} value={_title} className={classes}></input>
						</td>
						<td style={{'width':`${sdata.d_col_2}px`}}>
							<input style={{'display': 'inline'}} onChange={ (event) => onChangeHandler(event, setCaption)} value={_caption} className={classes}></input>
							<button onClick={ () => { CREATE() }} className="mx-2 py-1 px-1 bg-gray-50 hover:bg-white text-gray-800 border border-gray-400 rounded shadow" style={{'position': 'absolute', 'display': 'inline'}}>CREATE</button>
						</td>
				</tr>
			</>
		)
}

function Caption({caption, sdata, index}) {

 const [edit_caption, setEditCaption] = useState(false)
 const [edit_title, setEditTitle] = useState(false)

 const [_caption, setCaption] = useState(caption.caption)
 const [_title, setTitle] = useState(caption.caption_title)

 const isMounted = useRef(false)

 function onChangeHandler(event, setter) {
		setter(event.target.value)
	}

	// add a delay, then execute the api call on cleanup
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
			if (isMounted.current) {
			  UPDATE()
			} else {
					isMounted.current = true
				}
    }, 1500)
		return( () => clearTimeout(delayDebounceFn) )
  }, [_caption, _title])




	const UPDATE = () => {
		fetch(CONTEXT.edit_caption_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: "POST",
			headers: {
		    "Content-Type": "application/json",
				"Accept": 'application/json',
				'Authorization': `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token
						},
			body: JSON.stringify({'data': {
				'id': caption.id,
				'caption_title': _title,
				'caption': _caption
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
	}

	const classes="shadow appearance-none border rounded w-full py-1 text-gray-700 leading-tight focus:outline-none focus:shadow-outliney-1"

return(
		<>
					<tr className="hover:bg-gray-50 text-gray-400 text-left">
						{ edit_title ?
							<td>
								<input onChange={ (event) => onChangeHandler(event, setTitle)} value={_title} className={classes}></input>
							</td> :
							<td onClick={ () => { setEditTitle(true) } } style={{'width':`${sdata.d_col_1}px`}}> { _title } </td>
						}
						{ edit_caption ?
							<td>
								<input onChange={ (event) => onChangeHandler(event, setCaption)} value={_caption} className={classes}></input>
							</td> :
							<td onClick={ () => { setEditCaption(true) } } style={{'width':`${sdata.d_col_2}px`}}> { _caption } </td>
						}
					</tr>
				</>
		)
}
