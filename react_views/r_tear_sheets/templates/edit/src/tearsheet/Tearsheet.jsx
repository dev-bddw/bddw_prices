import { useRef, useState, useEffect } from 'react';

import TemplateA from './TemplateA';
import TemplateB from './TemplateB';
import TemplateC from './TemplateC';
import Image from './Image';
import Heading from './Heading';
import Captions from './Captions';
import Details from './Details';
import FooterDetails from './FooterDetail';
import ConfigPanel from './ConfigPanel';
import { createLegacyLeaf, updateNodeAtPath, setLeafAtPath } from './paneLayout';

export default function Tearsheet() {
	const [price_records, setPriceRecords] = useState(CONTEXT.tearsheet.price_records);
	const [showCreateInputs, setShowCreateInputs] = useState(true);
	const captions = CONTEXT.tearsheet.captions;
	const details = CONTEXT.tearsheet.details;
	const footer_details = CONTEXT.tearsheet.footer_details;
	const img = CONTEXT.tearsheet.img;
	const title = CONTEXT.tearsheet.title;

	const [selectedPanePath, setSelectedPanePath] = useState([]);

	const [sdata, setSheetData] = useState({
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

	const effectiveLayout = sdata.pane_layout ?? createLegacyLeaf(img, sdata.image_scale, sdata.image_offset_x, sdata.image_offset_y);

	const onLayoutChange = (path, updater) => {
		const current = sdata.pane_layout ?? createLegacyLeaf(img, sdata.image_scale, sdata.image_offset_x, sdata.image_offset_y);
		const newLayout = path.length === 0 ? updater(current) : updateNodeAtPath(current, path, updater);
		setSheetData((prev) => ({ ...prev, pane_layout: newLayout }));
	};

	const onUploadPaneImage = (path, file) => {
		const formData = new FormData();
		formData.append('image', file);
		formData.append('pane_path', JSON.stringify(path));
		fetch(CONTEXT.edit_pane_image_api, {
			credentials: 'include',
			mode: 'same-origin',
			method: 'POST',
			headers: {
				Authorization: `Token ${CONTEXT.auth_token}`,
				'X-CSRFToken': CONTEXT.csrf_token,
			},
			body: formData,
		})
			.then((r) => {
				if (!r.ok) return r.json().then((d) => { throw new Error(d.error || r.statusText); });
				return r.json();
			})
			.then((data) => {
				if (data.url) {
					setSheetData((prev) => ({
						...prev,
						pane_layout: setLeafAtPath(prev.pane_layout, path, { imageUrl: data.url }),
					}));
				}
			})
			.catch((err) => console.error('Pane image upload failed:', err));
	};

	const [template, setTemplate] = useState(CONTEXT.tearsheet.template)

	const renderTemplate = (template) => {
		{ switch(template) {
				case 'A':
				  // ONE COLUMN DISPLAY		(four column view)
					return(<TemplateA sdata={sdata} price_records={price_records}/>)
				case 'B':
					// TWO COLUMN DISPLAY (default tearsheet display -- 5 column view)
					return(<TemplateB sdata={sdata} price_records={price_records} setPriceRecords={setPriceRecords} tearsheet_id={CONTEXT.tearsheet.id}/>)
				case 'C':
				  // RULE DISPLAY ABOVE (four column view)
					return(<TemplateC sdata={sdata} price_records={price_records}/>)
		}}
	}

  return(
		<div>
			<table>
				<thead>
					<tr>
						<th></th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td style={{
							'padding-right': '75px',
							'padding-left': '75px',
							'width':'816px',
							'line-height': '1.5',
							'font-weight': '400',
							'letter-spacing': '.05em',
							'font-size': `${sdata.font_size}px`
							}} className="align-top">
								<Heading title={CONTEXT.tearsheet.title}/>
								<Image
									img={img}
									sdata={sdata}
									setSheetData={setSheetData}
									effectiveLayout={effectiveLayout}
									selectedPanePath={selectedPanePath}
									setSelectedPanePath={setSelectedPanePath}
									onLayoutChange={onLayoutChange}
									onUploadPaneImage={onUploadPaneImage}
								/>
								<Captions showCreateInputs={showCreateInputs} sdata={sdata} captions={captions} />
								<Details showCreateInputs={showCreateInputs} sdata={sdata} details={details}/>
								{renderTemplate(template) }
								<FooterDetails showCreateInputs={showCreateInputs} sdata={sdata} footers={footer_details} />
						</td>
						<td className="align-top">
								<ConfigPanel
									showCreateInputs={showCreateInputs}
									setShowCreateInputs={setShowCreateInputs}
									template={template}
									setTemplate={setTemplate}
									sdata={sdata}
									setSheetData={setSheetData}
									hasImage={!!img}
									effectiveLayout={effectiveLayout}
									selectedPanePath={selectedPanePath}
									setSelectedPanePath={setSelectedPanePath}
								/>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
			)
}
