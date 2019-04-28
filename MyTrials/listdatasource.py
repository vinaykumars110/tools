import ui
import Image


class MyTableViewDataSourc (ui.View):
	def tableview_cell_for_row(self,tableview,section,row):
		cell=ui.TableViewCell()
		cell.image_view.image=ui.Image.named('6.jpg')
		return cell
		

data=['vinay1','vinay2']

datasource = ui.ListDataSource(data)
datasource.image=ui.Image.named('6.jpg')

v = ui.load_view()
v['tableview1'].data_source=ui.Image.named('6.jpg')
v.present('sheet')
