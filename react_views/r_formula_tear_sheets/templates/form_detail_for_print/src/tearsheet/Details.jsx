import {useRef, useState, useEffect} from 'react';
import SETTINGS from './Settings'

function Details({details, sdata}) {
	return(
    <>
			<div style={{'height': sdata.pt_detail}}/>
	  <table style={{'width': '850px'}} className="mx-auto table-auto">
	  	<thead className="text-gray-400 text-left">
				<th></th>
				<th></th>
				<th></th>
				<th></th>
				<th></th>
			</thead>
			<tbody>
				{  details.map(  ( obj )  => { return( Object.entries(obj).map( ([key, value]) => { return( <DetailGroup sdata={sdata} details={value} name={key} />)}))})}
			</tbody>
		</table>
		</>
	)
}

export default Details;


function DetailGroup ({sdata, details, name}) {

	return(
		<>
			{ details.map( (detail, index) => {
				return(
					<DetailRow sdata={sdata} detail={detail} name={name} index={index}/>
					)
			})}
		</>
	)
}


function DetailRow({sdata, detail, name, index}) {
	const [edit_name, setEditName] = useState(false)
  const [edit_details, setEditDetails] = useState(false)

	const [_name, setName] = useState(detail.name)
	const [_details, setDetails] = useState(detail.details)

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


	const CREATE = () => {
		fetch(CONTEXT.create_detail_api, {
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
				'id': detail.id,
				'name': _name,
				'details': _details
			} }),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
	}

	const UPDATE = () => {
		fetch(CONTEXT.edit_detail_api, {
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
				'id': detail.id,
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
							<td onClick={ () => { setEditName(true) } } style={{'width':`${sdata.d_col_1}px`}}> { index == 0 ? _name : null} </td>
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
