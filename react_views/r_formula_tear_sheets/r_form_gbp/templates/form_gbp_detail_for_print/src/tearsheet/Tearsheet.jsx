import {useRef, useState, useEffect} from 'react'

import TemplateA from './TemplateA'
import TemplateB from './TemplateB'
import TemplateC from './TemplateC'
import Image from './Image'
import Heading from './Heading'
import Captions from './Captions'
import Details from './Details'
import FooterDetails from './FooterDetail'
import Footer from './Footer'

export default function Tearsheet() {

	const [price_records, setPriceRecords] = useState(CONTEXT.tearsheet.price_records)
  const captions = CONTEXT.tearsheet.captions
	const details = CONTEXT.tearsheet.details
	const footer_details = CONTEXT.tearsheet.footer_details
	const tearsheet_id = CONTEXT.tearsheet.id
	const img = CONTEXT.tearsheet.img
	const title = CONTEXT.tearsheet.title

	const [sdata, setSheetData] = useState( {
		'd_col_1': CONTEXT.tearsheet.sdata.d_col_1,
		'd_col_2': CONTEXT.tearsheet.sdata.d_col_2,
		'col_1': CONTEXT.tearsheet.sdata.col_1,
		'col_2': CONTEXT.tearsheet.sdata.col_2,
		'col_3': CONTEXT.tearsheet.sdata.col_3,
		'col_4': CONTEXT.tearsheet.sdata.col_4,
		'col_5': CONTEXT.tearsheet.sdata.col_5,
		'col_6': CONTEXT.tearsheet.sdata.col_6,
		'col_7': CONTEXT.tearsheet.sdata.col_7,
		'pt_cap': CONTEXT.tearsheet.sdata.pt_cap,
		'pt_detail': CONTEXT.tearsheet.sdata.pt_detail,
		'pt_footer': CONTEXT.tearsheet.sdata.pt_footer,
		'pt_pr': CONTEXT.tearsheet.sdata.pt_pr,
		'pt': CONTEXT.tearsheet.sdata.pt,
		'font_size': CONTEXT.tearsheet.sdata.font_size
		}
	)

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
							'padding-right': '75px',
							'padding-left': '75px',
							'width':'816px',
							'line-height': '1.5',
							'font-weight': '400',
							'letter-spacing': '.05em',
							'font-size': `${sdata.font_size}px`
							}}>
								<Heading title={CONTEXT.tearsheet.title}/>
								<Image img={img}/>
								<Captions sdata={sdata} captions={captions} />
								<Details sdata={sdata} details={details}/>
								{renderTemplate(template) }
								<FooterDetails sdata={sdata} footers={footer_details} />
								<Footer/>
						</td>
						<td>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
			)
}
