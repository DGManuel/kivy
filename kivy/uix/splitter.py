'''
Splitter
======

.. image:: images/Splitter.jpg
:align: right

:class:`Splitter` is a :class:`~kivy.uix.widget.Widget` with associated actions
that are triggered when it's pressed and moved.
To configure, you can set 'adjust_from' to 'left' or 'right' or 'top'
or 'bottom'.

Usage:

splitter = Splitter(sizable_from = 'right')
splitter.add_widget(layout_or_widget_instance)
splitter.min_size = 100
splitter.max_size = 250
'''


__all__ = ('Splitter', )

from kivy.uix.button import Button
from kivy.properties import OptionProperty, NumericProperty, ObjectProperty,\
    ListProperty
from kivy.uix.boxlayout import BoxLayout


class SplitterStrip(Button):
    pass


class Splitter(BoxLayout):
    '''This is a Splitter widget used for resizing it's children
    set `adjust_from to` `left`/`right`/`top` or `bottom`
    The parent Layout will now be re-sizable by clicking/touching
    on this resize widget and moving.
    '''

    color = ListProperty([1, 0, 0, .5])
    '''color, in the format (r, g, b, a).

    :data:`color` is a :class:`~kivy.properties.ListProperty`,
    default to [1, 1, 1, 1].
    '''

    strip_cls = ObjectProperty(SplitterStrip)
    '''Specifies the class of the resize Strip

    :data: `strip_cls` is a :class:`kivy.properties.ObjectProperty`
    defaults to SplitterStrip
    '''

    sizable_from = OptionProperty('left',
        options=('left', 'right', 'top', 'bottom'))
    '''Specifies weather the widget is resizable from ::
        `left`, `right`, `top` or `bottom`

    :data:`sizable_from` is a :class:`~kivy.properties.OptionProperty`
    defaults to `left`
    '''

    strip_size = NumericProperty('10pt')
    '''Specifies the size of resize strip

    :data:`strp_size` is a :class:`~kivy.properties.NumericProperty`
    defaults to `10pt`
    '''

    min_size = NumericProperty('100pt')
    '''Specifies the minimum size beyound which the widget is not resizable

    :data:`min_size` is a :class:`~kivy.properties.NumericProperty`
    defaults to `100pt`
    '''

    max_size = NumericProperty('500pt')
    '''Specifies the maximum size beyound which the widget is not resizable

    :data:`max_size` is a :class:`~kivy.properties.NumericProperty`
    defaults to `500pt`
    '''

    def __init__(self, **kwargs):
        self._container = None
        self._strip = None
        super(Splitter, self).__init__(**kwargs)

    def on_sizable_from(self, instance, sizable_from):
        if not self._container:
            return

        sup = super(Splitter, self)
        _strp = self._strip
        if _strp:
            sup.remove_widget(self._strip)
        else:
            self._strip = _strp = self.strip_cls()

        sz_frm = self.sizable_from[0]
        if sz_frm in ('l', 'r'):
            _strp.size_hint = None, 1
            _strp.width = self.strip_size
            self.unbind(strip_size=_strp.setter('width'))
            self.bind(strip_size=_strp.setter('width'))
        else:
            _strp.size_hint = 1, None
            _strp.height = self.strip_size
            self.orientation = 'vertical'
            self.unbind(strip_size=_strp.setter('height'))
            self.bind(strip_size=_strp.setter('height'))

        index = 1
        if sz_frm in ('r', 'b'):
            index = 0
        sup.add_widget(_strp, index)

        _strp.unbind(on_touch_down=self.strip_down)
        _strp.unbind(on_touch_move=self.strip_move)
        _strp.unbind(on_touch_up=self.strip_up)
        _strp.bind(on_touch_down=self.strip_down)
        _strp.bind(on_touch_move=self.strip_move)
        _strp.bind(on_touch_up=self.strip_up)

    def add_widget(self, widget, index=0):
        if self._container or not widget:
            return Exception('Splitter accepts only one Widget')
        self._container = widget
        sz_frm = self.sizable_from[0]
        if sz_frm in ('l', 'r'):
            widget.size_hint_x = 1
        else:
            widget.size_hint_y = 1

        index = 0
        if sz_frm in ('r', 'b'):
            index = 1
        super(Splitter, self).add_widget(widget, index)
        self.on_sizable_from(self, self.sizable_from)

    def remove_widget(self, widget, *largs):
        super(Splitter, self).remove_widget(widget)
        if widget == self._container:
            self._container = None

    def clear_widgets(self):
        self.remove_widget(self._container)

    def strip_up(self, instance, touch):
        if (not self.collide_point(*touch.pos)):
            return False
        touch.grab(self)
        pos = touch.pos

    def strip_move(self, instance, touch):
        if touch.grab_current is not self._strip:
            return False
        sign = 1
        max_size = self.max_size
        min_size = self.min_size
        sz_frm = self.sizable_from[0]

        if sz_frm in ('t', 'b'):
            diff_y = (touch.dy)
            if sz_frm == 'b':
                sign = -1
            if not self.size_hint_y:
                if self.height > 0:
                    self.height += sign * diff_y
                else:
                    self.height = 1
            else:
                diff = (diff_y / self.parent.height)
                self.size_hint_y += sign * (diff)
            height = self.height
            if height > max_size:
                self.height = max_size
            elif height < min_size:
                self.height = min_size
        else:
            diff_x = (touch.dx)
            if sz_frm == 'l':
                sign = -1
            if not self.size_hint_x:
                if self.width > 0:
                    self.width += sign * (diff_x)
                else:
                    self.width = 1
            else:
                diff = (diff_x / self.parent.width)
                self.size_hint_x += sign * (diff)

            width = self.width
            if width > max_size:
                self.width = max_size
            elif width < min_size:
                self.width = min_size

    def strip_down(self, instance, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.floatlayout import FloatLayout

    class SplitterApp(App):

        def build(self):
            root = FloatLayout()
            bx = BoxLayout()
            bx.add_widget(Button())
            bx.add_widget(Button())
            bx2 = BoxLayout()
            bx2.add_widget(Button())
            bx2.add_widget(Button())
            bx2.add_widget(Button())
            spl = Splitter(
                size_hint=(1, .25),
                pos_hint = {'top': 1},
                sizable_from = 'bottom')
            spl1 = Splitter(
                sizable_from='left',
                size_hint=(None, 1), width=90)
            spl1.add_widget(Button())
            bx.add_widget(spl1)
            spl.add_widget(bx)

            spl2 = Splitter(size_hint=(.25, 1))
            spl2.add_widget(bx2)
            spl2.sizable_from = 'right'
            root.add_widget(spl)
            root.add_widget(spl2)
            return root

    SplitterApp().run()
