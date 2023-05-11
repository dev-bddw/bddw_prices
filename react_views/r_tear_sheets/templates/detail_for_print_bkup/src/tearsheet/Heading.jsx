import { useState, useRef, useEffect } from 'react';
import SETTINGS from './Settings'

export default function Heading({title}) {

	const links = [
		{
		'name': 'VIEW PDF',
		'href': CONTEXT.print,
		},
		{
		'name': 'DOWNLOAD PDF',
		'href': CONTEXT.print + '?justDownload=True',
	  },
		{
		'name': 'VIEW LIST PDF',
		'href': CONTEXT.print_list,
		},
		{
		'name': 'DOWNLOAD LIST PDF',
		'href': CONTEXT.print_list + '?justDownload=True',
		},
		{
		'name': 'EDIT',
		'href': CONTEXT.edit_tearsheet,
		}
	]


	return (
		<div className="text-left">
			<span style={{'display': 'block', 'font-size': '30px'}} className="text-gray-500 w-full py-2 text-left">{title}</span>
	</div>
	)
}
