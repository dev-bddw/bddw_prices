import { useRef, useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Switch from '@mui/material/Switch';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@mui/material/Button';

import { canSplit, replaceLeafWithSplit, hasSplit, getLeafAtPath, setLeafAtPath, canRemoveLeaf, removeLeaf } from './paneLayout';

const NUDGE_STEP = 10;

export default function ConfigPanel({ showCreateInputs, setShowCreateInputs, template, setTemplate, sdata, setSheetData, hasImage, effectiveLayout, selectedPanePath, setSelectedPanePath }) {

	const default_values = {
		'font_size': 10,
		'pt_cap': 5,
		'd_col_1': 83,
		'd_col_2': 703,
		'pt_detail': 5,
		'pt_pr': 5,
		'col_1': 87,
		'col_2': 173,
		'col_3': 499,
		'col_4': 80,
		'col_5': 54,
		'pt_footer': 5,
		'image_scale': 1,
		'image_offset_x': 0,
		'image_offset_y': 0,
		'pane_layout': null,
		'image_gutter_width': 8,
	};

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
		'font_size': 'Font Size'
	}

	const initial_values = useRef({
		'font_size': CONTEXT.tearsheet.sdata.font_size,
		'pt_cap': CONTEXT.tearsheet.sdata.pt_cap,
		'd_col_1': CONTEXT.tearsheet.sdata.d_col_1,
		'd_col_2': CONTEXT.tearsheet.sdata.d_col_2,
		'pt_detail': CONTEXT.tearsheet.sdata.pt_detail,
		'pt_pr': CONTEXT.tearsheet.sdata.pt_pr,
		'col_1': CONTEXT.tearsheet.sdata.col_1,
		'col_2': CONTEXT.tearsheet.sdata.col_2,
		'col_3': CONTEXT.tearsheet.sdata.col_3,
		'col_4': CONTEXT.tearsheet.sdata.col_4,
		'col_5': CONTEXT.tearsheet.sdata.col_5,
		'pt_footer': CONTEXT.tearsheet.sdata.pt_footer,
		'image_scale': CONTEXT.tearsheet.sdata.image_scale != null ? CONTEXT.tearsheet.sdata.image_scale : 1,
		'image_offset_x': CONTEXT.tearsheet.sdata.image_offset_x != null ? CONTEXT.tearsheet.sdata.image_offset_x : 0,
		'image_offset_y': CONTEXT.tearsheet.sdata.image_offset_y != null ? CONTEXT.tearsheet.sdata.image_offset_y : 0,
		'pane_layout': CONTEXT.tearsheet.sdata.pane_layout ?? null,
		'image_gutter_width': CONTEXT.tearsheet.sdata.image_gutter_width ?? 8,
	});

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

	const handleChange = (event, key) => {
	  const updatedValue = { [key] : event.target.value }
		setSheetData( sdata => ({
			...sdata,
			...updatedValue
		}));
	}

	// MUI Slider passes (event, value); use value so font_size and numeric configs update correctly
	const handleSliderChange = (event, value, key) => {
		setSheetData(prev => ({ ...prev, [key]: value }));
	}

	const hasMultiPane = effectiveLayout && sdata?.pane_layout != null;
	const selectedLeaf = hasMultiPane && selectedPanePath?.length != null ? getLeafAtPath(effectiveLayout, selectedPanePath) : null;
	const showPositionImage = (hasImage && !hasMultiPane) || (hasMultiPane && selectedLeaf != null);
	const canSplitCurrent = effectiveLayout && canSplit(effectiveLayout, selectedPanePath ?? []);
	const showGutterWidth = effectiveLayout && hasSplit(effectiveLayout);
	const layoutForRemove = sdata?.pane_layout ?? effectiveLayout;
	const canRemoveCurrent = hasMultiPane && layoutForRemove && selectedPanePath != null && selectedPanePath.length > 0 && canRemoveLeaf(layoutForRemove, selectedPanePath);

	const handleImageScaleChange = (event, value) => {
		const v = Math.max(1, value);
		if (hasMultiPane && selectedPanePath?.length != null) {
			setSheetData((prev) => ({ ...prev, pane_layout: setLeafAtPath(prev.pane_layout, selectedPanePath, { image_scale: v }) }));
		} else {
			setSheetData((prev) => ({ ...prev, image_scale: v }));
		}
	};

	const nudge = (dx, dy) => {
		if (hasMultiPane && selectedPanePath?.length != null) {
			const leaf = getLeafAtPath(sdata.pane_layout, selectedPanePath);
			setSheetData((prev) => ({
				...prev,
				pane_layout: setLeafAtPath(prev.pane_layout, selectedPanePath, {
					image_offset_x: (leaf?.image_offset_x ?? 0) + dx,
					image_offset_y: (leaf?.image_offset_y ?? 0) + dy,
				}),
			}));
		} else {
			setSheetData((prev) => ({
				...prev,
				image_offset_x: (prev.image_offset_x || 0) + dx,
				image_offset_y: (prev.image_offset_y || 0) + dy,
			}));
		}
	};

	const positionZoomValue = showPositionImage && (hasMultiPane ? (selectedLeaf?.image_scale ?? 1) : (sdata.image_scale ?? 1));

	const handleGutterWidthChange = (event, value) => {
		setSheetData((prev) => ({ ...prev, image_gutter_width: value }));
	};

	const handleSplit = (direction) => {
		const nextLayout = replaceLeafWithSplit(sdata.pane_layout ?? effectiveLayout, selectedPanePath ?? [], direction);
		setSheetData((prev) => ({ ...prev, pane_layout: nextLayout }));
		setSelectedPanePath?.([]);
	};

	const handleRemoveFrame = () => {
		if (!canRemoveCurrent || !layoutForRemove) return;
		const nextLayout = removeLeaf(layoutForRemove, selectedPanePath);
		setSheetData((prev) => ({ ...prev, pane_layout: nextLayout }));
		setSelectedPanePath?.([]);
	};

	const sliderKeys = Object.keys(sdata).filter(key => easy_defs[key] != null)

	return(
		<div className="confg_wrapper drop-shadow-xl" style={{ margin: '0', width: '475px', padding: '24px 0' }}>
			<div className="px-5 bg-gray-50 border border-solid rounded-lg text-left">
				<h3 className="font-bold py-3">CONFIG</h3>
				<TemplateDropdown  template={template} setTemplate={setTemplate}/>
				<InputSwitch  showCreateInputs={showCreateInputs} setShowCreateInputs={setShowCreateInputs}/>
				{showPositionImage && (
					<div style={{ paddingTop: '20px', paddingBottom: '20px' }}>
						<h4 className="font-semibold text-slate-600 py-2">Position image</h4>
						<Box sx={{ width: 400, color: 'black' }}>
							<p className="font-sans text-slate-400 py-2 text-s">Zoom ({positionZoomValue})</p>
							<Slider size="small" aria-label="image-zoom" min={1} max={3} step={0.1} value={Math.max(1, positionZoomValue ?? 1)} onChange={handleImageScaleChange} />
						</Box>
						<p className="font-sans text-slate-400 py-2 text-s">Move</p>
						<div className="flex gap-2 flex-wrap">
							<Button size="small" variant="outlined" onClick={() => nudge(-NUDGE_STEP, 0)}>Left</Button>
							<Button size="small" variant="outlined" onClick={() => nudge(NUDGE_STEP, 0)}>Right</Button>
							<Button size="small" variant="outlined" onClick={() => nudge(0, -NUDGE_STEP)}>Up</Button>
							<Button size="small" variant="outlined" onClick={() => nudge(0, NUDGE_STEP)}>Down</Button>
						</div>
					</div>
				)}
				{canSplitCurrent && (
					<div style={{ paddingTop: '20px', paddingBottom: '20px' }}>
						<h4 className="font-semibold text-slate-600 py-2">Split frame</h4>
						<div className="flex gap-2 flex-wrap">
							<Button size="small" variant="outlined" onClick={() => handleSplit('horizontal')}>Split horizontally</Button>
							<Button size="small" variant="outlined" onClick={() => handleSplit('vertical')}>Split vertically</Button>
						</div>
					</div>
				)}
				{hasMultiPane && selectedPanePath != null && selectedPanePath.length > 0 && (
					<div style={{ paddingTop: '20px', paddingBottom: '20px' }}>
						<h4 className="font-semibold text-slate-600 py-2">Remove frame</h4>
						<p className="font-sans text-slate-400 py-2 text-s">Remove the selected pane. Only allowed when the adjacent pane is a single frame (keeps borders straight).</p>
						<Button size="small" variant="outlined" color="secondary" onClick={handleRemoveFrame} disabled={!canRemoveCurrent}>
							Remove selected frame
						</Button>
					</div>
				)}
				{showGutterWidth && (
					<div style={{ paddingTop: '20px', paddingBottom: '20px' }}>
						<h4 className="font-semibold text-slate-600 py-2">Gutter width between frames</h4>
						<Box sx={{ width: 400, color: 'black' }}>
							<p className="font-sans text-slate-400 py-2 text-s">Width of the divider between panes (pixels)</p>
							<Slider size="small" aria-label="gutter-width" min={0} max={32} step={1} value={sdata.image_gutter_width ?? 8} onChange={handleGutterWidthChange} valueLabelDisplay="auto" valueLabelFormat={(v) => `${v}px`} />
						</Box>
					</div>
				)}
				{ sliderKeys.map( (key) => {
					return(
						<Box key={key} sx={{ width: 400, color: 'black' }}>
							<p className="font-sans text-slate-400 py-2 text-s">{easy_defs[key]} ({sdata[key]}) </p>
							<Slider size="small" aria-label="col-width" max={ key == 'font_size' ? 30 : 1000} value={Number(sdata[key])} onChange={ (event, value) => handleSliderChange(event, value, key) } />
					</Box>
					)})
				}
				<div style={{'height': '40px'}}></div>
				<div style={{ letterSpacing: '1', fontSize: '14px', display: 'flex', flexWrap: 'wrap', gap: '12px' }} className="text-left">
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
