#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from Qt import QtCore, QtGui, QtWidgets

from NodeGraphQt import (NodeGraph,
                         BaseNode,
                         BackdropNode,
                         GroupNode,
                         PropertiesBinWidget,
                         NodesTreeWidget)

# import example nodes from the "example_nodes" package
from examples.custom_nodes import basic_nodes, widget_nodes


def draw_triangle_port(painter, rect, info):
    """
    Custom paint function for drawing a Triangle shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    size = int(rect.height() / 2)
    triangle = QtGui.QPolygonF()
    triangle.append(QtCore.QPointF(-size, size))
    triangle.append(QtCore.QPointF(0.0, -size))
    triangle.append(QtCore.QPointF(size, size))

    transform = QtGui.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()


def draw_square_port(painter, rect, info):
    """
    Custom paint function for drawing a Square shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35, 255)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()


class MyNode(BaseNode):
    """
    example test node.
    """

    # set a unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set the initial default node name.
    NODE_NAME = 'my node'

    def __init__(self):
        super(MyNode, self).__init__()
        self.set_color(25, 58, 51)

        # create input and output port.
        self.add_input('in port', color=(200, 10, 0))
        self.add_output('default port')
        self.add_output('square port', painter_func=draw_square_port)
        self.add_output('triangle port', painter_func=draw_triangle_port)


class MyGroup(GroupNode):
    """
    example test group node.
    """

    # set a unique node identifier.
    __identifier__ = 'com.chantasticvfx'

    # set the initial default node name.
    NODE_NAME = 'group node'

    def __init__(self):
        super(MyGroup, self).__init__()
        self.set_color(50, 8, 25)

        # create input and output port.
        self.add_input('in')
        self.add_output('out')


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])

    # create node graph.
    graph = NodeGraph()

    # widget used for the node graph.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()


    # show the properties bin when a node is "double clicked" in the graph.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)
    def show_prop_bin(node):
        if not properties_bin.isVisible():
            properties_bin.show()
    graph.node_double_clicked.connect(show_prop_bin)


    # show the nodes list when a node is "double clicked" in the graph.
    node_tree = NodesTreeWidget(node_graph=graph)
    node_tree.set_category_label('nodes.widget', 'Widget Nodes')
    def show_nodes_list(node):
        if not node_tree.isVisible():
            node_tree.update()
            node_tree.show()
    graph.node_double_clicked.connect(show_nodes_list)


    # registered nodes.
    nodes_to_reg = [
        MyNode, MyGroup,
        basic_nodes.FooNode,
        basic_nodes.BarNode,
        widget_nodes.DropdownMenuNode,
        widget_nodes.TextInputNode,
        widget_nodes.CheckboxNode
    ]
    graph.register_nodes(nodes_to_reg)

    # register backdrop node with "Backdrop" alias.
    graph.register_node(BackdropNode, 'Backdrop')

    my_node = graph.create_node(
        'com.chantasticvfx.MyNode',
        name='chantastic!',
        color='#0a1e20',
        text_color='#feab20'
    )

    foo_node = graph.create_node(
        'nodes.basic.FooNode',
        name='node')
    foo_node.set_disabled(True)

    # create example "TextInputNode".
    text_node = graph.create_node(
        'nodes.widget.TextInputNode',
        name='text node')

    # create example "TextInputNode".
    checkbox_node = graph.create_node(
        'nodes.widget.CheckboxNode',
        name='checkbox node')

    # create node with a combo box menu.
    menu_node = graph.create_node(
        'nodes.widget.DropdownMenuNode',
        name='menu node')

    # change node icon.
    this_path = os.path.dirname(os.path.abspath(__file__))
    icon = os.path.join(this_path, 'example_nodes', 'pear.png')
    icon_node = graph.create_node('nodes.basic.BarNode')
    icon_node.set_icon(icon)
    icon_node.set_name('icon node')

    # create the group node
    group_node = graph.create_node('com.chantasticvfx.MyGroup')

    # connect the nodes.
    foo_node.set_output(0, icon_node.input(2))
    foo_node.set_output(1, checkbox_node.input(0))
    text_node.set_output(0, checkbox_node.input(0))
    text_node.set_output(0, group_node.input(0))
    menu_node.set_input(0, icon_node.output(1))
    icon_node.set_input(0, text_node.output(0))

    # auto layout nodes.
    graph.auto_layout_nodes()

    # wrap a backdrop node.
    backdrop_node = graph.create_node('Backdrop')
    backdrop_node.wrap_nodes([icon_node, menu_node])

    graph.fit_to_selection()

    app.exec_()