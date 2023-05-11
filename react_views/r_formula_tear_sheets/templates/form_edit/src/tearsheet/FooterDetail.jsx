import {useRef, useState, useEffect} from 'react';
import SETTINGS from './Settings'

export default function FooterDetails({showCreateInputs, footers, sdata}) {
	return(
    <>
		<div style={{'height': sdata.pt_footer}}/>
			<table className="table-auto">
				<thead className="text-gray-400 text-left">
					<th></th>
					<th></th>
					<th></th>
					<th></th>
					<th></th>
				</thead>
				<tbody>
				{  footers.map(  ( footer )  => { return( <FooterRow sdata={sdata} footer={footer} />)})}
				{ showCreateInputs ?  <AddFooterDetail sdata={sdata}/> : null }
				</tbody>
		</table>
		</>
	)
}

function AddFooterDetail({sdata}) {

  const [_name, setName] = useState('')
	const [_details, setDetails] = useState('FOOTER DETAILS')
	const [_id, setId] = useState('')

	const CREATE = () => {
		fetch(CONTEXT.create_footer_api, {
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
				'name': _name,
				'details': _details
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
		window.location.reload()
		//TODO: api returns new caption ID, then update the list of captions with the new caption values
		//TODO: instead we just update page
	}

	function onChangeHandler(event, setter) {
			setter(event.target.value)
	}

	return(
			<>
				<tr className="hover:bg-gray-50 text-gray-400 text-left">
						<td style={{'width':`${sdata.d_col_1}px`}}>
							<input onChange={ (event) => onChangeHandler(event, setName)} value={_name} className={SETTINGS.input_classes}></input>
						</td>
						<td style={{'width':`${sdata.d_col_2}px`}}>
							<input style={{'display': 'inline'}} onChange={ (event) => onChangeHandler(event, setDetails)} value={_details} className={SETTINGS.input_classes}></input>
							<button onClick={ () => { CREATE() }} className="mx-2 py-1 px-1 bg-gray-50 hover:bg-white text-gray-800 border border-gray-400 rounded shadow" style={{'position': 'absolute', 'display': 'inline'}}>CREATE</button>
						</td>
				</tr>
			</>
		)
}


function FooterRow({sdata, footer, index}) {
	const [edit_name, setEditName] = useState(false)
  const [edit_details, setEditDetails] = useState(false)

	const [_name, setName] = useState(footer.name)
	const [_details, setDetails] = useState(footer.details)

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
  }, [_name, _details])

	const UPDATE = () => {
		fetch(CONTEXT.edit_footer_api, {
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
				'id': footer.id,
				'name': _name,
				'details': _details
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
	}


return(
				<>
					<tr className="hover:bg-gray-50 text-gray-400 text-left">
						{ edit_name ?
							<td>
								<input onChange={ (event) => onChangeHandler(event, setName)} value={_name} className={SETTINGS.input_classes}></input>
							</td> :
							<td onClick={ () => { setEditName(true) } } style={{'width':`${sdata.d_col_1}px`}}>{_name}</td>
						}
						{ edit_details ?
							<td>
								<input onChange={ (event) => onChangeHandler(event, setDetails)} value={_details} className={SETTINGS.input_classes}></input>
							</td> :
							<td onClick={ () => { setEditDetails(true) } } style={{'width':`${sdata.d_col_2}px`}}>{_details} </td>
						}
					</tr>
				</>
		)
	}
