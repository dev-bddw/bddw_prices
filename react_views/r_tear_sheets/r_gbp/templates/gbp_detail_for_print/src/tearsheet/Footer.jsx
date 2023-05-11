export default function Footer() {

	const current_year = new Date().getFullYear()

	return(
		<div style={{'font-size': '10px', 'letter-spacing': '2px','left':'200px','top': '1355px', 'position': 'absolute'}} className='text-gray-400'>
			BDDW - 5 MOUNT STREET LONDON - T +44 (0) 20 3941 7300 - INFO@BDDW.COM - WWW.BDDW.COM - {current_year}
		</div>
	)
}
