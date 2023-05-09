import { useRef, useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Slider from '@mui/material/Slider';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Switch from '@mui/material/Switch';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';


export default function ConfigPanel({ showCreateInputs, setShowCreateInputs, template, setTemplate, sdata, setSheetData}) {

	const default_values ={
		'd_col_1': 87,
		'd_col_2': 703,
		'col_1': 87,
		'col_2': 173,
		'col_3': 499,
		'col_4': 80,
		'col_5': 54,
		'pt_cap': 5,
		'pt_detail': 5,
		'pt_footer': 5,
		'pt_pr': 5,
		'pt': 5,
		'font_size': 10
	}

	const initial_values = useRef( {
		'd_col_1': CONTEXT.tearsheet.sdata.d_col_1,
		'd_col_2': CONTEXT.tearsheet.sdata.d_col_2,
		'col_1': CONTEXT.tearsheet.sdata.col_1,
		'col_2': CONTEXT.tearsheet.sdata.col_2,
		'col_3': CONTEXT.tearsheet.sdata.col_3,
		'col_4': CONTEXT.tearsheet.sdata.col_4,
		'col_5': CONTEXT.tearsheet.sdata.col_5,
		'pt_cap': CONTEXT.tearsheet.sdata.pt_cap,
		'pt_detail': CONTEXT.tearsheet.sdata.pt_detail,
		'pt_footer': CONTEXT.tearsheet.sdata.pt_footer,
		'pt_pr': CONTEXT.tearsheet.sdata.pt_pr,
		'pt': CONTEXT.tearsheet.sdata.pt,
		'font_size': CONTEXT.tearsheet.sdata.font_size
	})

	const initial_template = useRef( template )

	const [message, setMessage] = useState('...')

	const [added, setAdded] = useState()

	useEffect( () => {
		let sum = sdata.col_1 + sdata.col_2 + sdata.col_3 + sdata.col_4 + sdata.col_5
		setAdded(sum)
	}, [sdata]
)



	const save = () => {
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
			body: JSON.stringify({
				'data': {
					'template': template,
					'sdata': sdata}}),
					})
						.then(response => response.json())
						.then(data => {
							console.log(data);
						})
		setMessage('Changes saved!')
		initial_values.current = sdata // update initail values after save or else DISCARD will discard all changes -- even the saved ones
		initial_template.current = template

	}

	const reset = () => {
		setSheetData(initial_values.current)
		setTemplate(initial_template.current)
		setMessage('Changes discarded.')
	}

	const defaults = () => {
		setSheetData(default_values)
		setTemplate('B')
		setMessage('Defaults applied. Not saved!')
	}

	const easy_defs = {
		'd_col_1': 'Details Column One Width',
		'd_col_2': 'Details Column Two Width',
		'col_1': 'Price Record Column One Width',
		'col_2': 'Price Record Column Two Width',
		'col_3': 'Price Record Column Three Width',
		'col_4': 'Price Record Column Four Width',
		'col_5': 'Price Record Column Five Width',
		'pt_cap': 'Padding Top Captions',
		'pt_detail': 'Padding Top Detail',
		'pt_footer': 'Padding Top Footer',
		'pt_pr': 'Padding Top Price Records',
		'pt': 'Padding top details/captions/footer',
		'font_size': 'Font Size'
	}


	const handleChange = (event, key) => {
	  const updatedValue = { [key] : event.target.value }
		setSheetData( sdata => ({
			...sdata,
			...updatedValue
		}));
	}

	// need to break these sliders into like groups
	// details columns
	// price records columns
	// misc
	return(
		<div className="confg_wrapper drop-shadow-xl" style={{'margin': '0 0 0 50px', 'width': '475px'}}>
		<div style={{'height': '85px'}}></div>
			<div className="px-5 bg-gray-50 border border-solid rounded-lg text-left">
				<h3 className="font-bold py-3">CONFIG</h3>
				<TemplateDropdown  template={template} setTemplate={setTemplate}/>
				<InputSwitch  showCreateInputs={showCreateInputs} setShowCreateInputs={setShowCreateInputs}/>
				{ Object.keys(sdata).map( (key) => {
					return(
						<Box sx={{ width: 400, color: 'black' }}>
							<p className="font-sans text-slate-400 py-2 text-s">{easy_defs[key]} ({sdata[key]}) </p>
							<Slider size="small" aria-label="col-width" max={ key == 'font_size' ? 30 : 1000} value={sdata[key]} defaultValue={sdata[key]} onChange={ (event) => handleChange(event,key) } />
					</Box>
					)})
				}
				<div style={{'height': '40px'}}></div>
				<div style={{'letter-spacing': '1','font-size': '14px' }} className="text-left">
					<button className="bg-gray-50 hover:bg-white text-gray-800 py-3 px-4 border border-gray-400 rounded shadow" onClick={ ()=> save() }>SAVE</button>
					<button className="bg-gray-50 hover:bg-white text-gray-800 py-3 px-4 border border-gray-400 rounded shadow" onClick={ ()=> reset() }>DISCARD CHANGES</button>
					<button className="bg-gray-50 hover:bg-white text-gray-800 py-3 px-4 border border-gray-400 rounded shadow" onClick={ ()=> defaults() }>DEFAULTS</button>
					<div style={{'display':'block'}}>
						<p className="py-5 text-xs text-green-600">{message}</p>
					</div>
				</div>
			</div>
		</div>
		);
	}
function InputSwitch({showCreateInputs, setShowCreateInputs}) {
// https://mui.com/material-ui/react-switch/

	const handleChange = () => {
		setShowCreateInputs(!showCreateInputs)
	}

	return(
		<div className="template__wrapper py-5">
			<FormGroup>
				<FormControlLabel control={
				<Switch checked={showCreateInputs} onChange={ () => handleChange() } inputProps={{'aria-label': 'controlled'}} />
				} label="Show Input Fields"/>
			</FormGroup>
		</div>
		)
}

function TemplateDropdown({template, setTemplate}) {
  //https://mui.com/material-ui/react-select/
	//
	const handleClick = (event) => {
		setTemplate(event)
	}


	return(
		<div className="template__wrapper py-5">
			<FormControl fullWidth>
				<InputLabel id="demo-simple-select-label">Template</InputLabel>
					<Select
					labelId="demo-simple-select-label"
					id="demo-simple-select"
					defaultValue={template}
		      value={template}
					label="Template"

					>
						<MenuItem onClick={ () => handleClick('A')} value='A'>One Column</MenuItem>
						<MenuItem onClick={ () => handleClick('B')} value='B'>Two Column</MenuItem>
						<MenuItem onClick={ () => handleClick('C')} value='C'>Rule Display Above</MenuItem>
					</Select>
			</FormControl>
		</div>
		)
}
