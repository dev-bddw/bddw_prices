import { useRef, useState, useEffect } from 'react';

import TemplateA from './TemplateA';
import TemplateB from './TemplateB';
import TemplateC from './TemplateC';
import Image from './Image';
import Heading from './Heading';
import Captions from './Captions';
import Details from './Details';
import FooterDetails from './FooterDetail';
import { createLegacyLeaf } from './paneLayout';

export default function Tearsheet() {
	const [price_records, setPriceRecords] = useState(CONTEXT.tearsheet.price_records);
	const captions = CONTEXT.tearsheet.captions;
	const details = CONTEXT.tearsheet.details;
	const footer_details = CONTEXT.tearsheet.footer_details;
	const img = CONTEXT.tearsheet.img;
	const title = CONTEXT.tearsheet.title;

	const rawSdata = CONTEXT.tearsheet.sdata || {};
	const [sdata, setSheetData] = useState({
		'd_col_1': rawSdata.d_col_1,
		'd_col_2': rawSdata.d_col_2,
		'col_1': rawSdata.col_1,
		'col_2': rawSdata.col_2,
		'col_3': rawSdata.col_3,
		'col_4': rawSdata.col_4,
		'col_5': rawSdata.col_5,
		'pt_cap': rawSdata.pt_cap,
		'pt_detail': rawSdata.pt_detail,
		'pt_footer': rawSdata.pt_footer,
		'pt_pr': rawSdata.pt_pr,
		'pt': rawSdata.pt,
		'font_size': rawSdata.font_size != null ? Number(rawSdata.font_size) : 12,
		'image_scale': rawSdata.image_scale,
		'image_offset_x': rawSdata.image_offset_x,
		'image_offset_y': rawSdata.image_offset_y,
		'pane_layout': rawSdata.pane_layout ?? null,
		'image_gutter_width': rawSdata.image_gutter_width ?? 8,
	});

	const effectiveLayout = sdata.pane_layout ?? createLegacyLeaf(img, sdata.image_scale, sdata.image_offset_x, sdata.image_offset_y);

	const [template, setTemplate] = useState(CONTEXT.tearsheet.template)

	const renderTemplate = (template) => {
		{ switch(template) {
				case 'A':
				  // ONE COLUMN DISPLAY		(four column view)
					return(<TemplateA sdata={sdata} price_records={price_records}/>)
				case 'B':
					// TWO COLUMN DISPLAY (default tearsheet display -- 5 column view)
					return(<TemplateB sdata={sdata} price_records={price_records}/>)
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
							paddingRight: '75px',
							paddingLeft: '75px',
							width: '816px',
							lineHeight: '1.5',
							fontWeight: '400',
							letterSpacing: '.05em',
						}}>
								<Heading title={CONTEXT.tearsheet.title}/>
								<Image
									img={img}
									sdata={sdata}
									effectiveLayout={effectiveLayout}
								/>
								<div className="tearsheet-content" style={{ fontSize: `${Number(sdata.font_size) || 12}px` }}>
									<Captions sdata={sdata} captions={captions} />
									<Details sdata={sdata} details={details}/>
									{renderTemplate(template) }
									<FooterDetails sdata={sdata} footers={footer_details} />
								</div>
						</td>
						<td>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
			)
}
