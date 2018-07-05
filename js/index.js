Vue.component('coursebox',{
  template:'#course',
  props:['course'],
  mounted:()=>{
    // console.log(this.course)
  },
  data:()=>{
    return {
      grade_color:['rgb(255, 128, 1)','rgb(111, 255, 0)','rgb(0, 165, 255)','rgb(247, 0, 255)']
    };
  },
  methods:{
    outline(){
      return this.course.outline;
    },
    color(){
      let font_color="color: ";
      return font_color+this.grade_color[parseInt(this.course.grade)-1];
    },
    ccuplus(){
      return 'https://ccu.plus/#!/courses/' + this.course.class_id;
    },
  }
});
const vm = new Vue({
  el:'#app',
  data:{
    faculties:['全部','文學院','理學院','社科院','工學院','管學院','法學院','教育學院','其他'],
    departments:[],
    codes:[],
    courses:[],
    faculty:'0',
    department:'0',
    filter:'',
    query_options:['課程名稱','老師名稱'],
    query_transalte:{'課程名稱':'class_name','老師名稱':'teacher'},
    selected:'課程名稱',
  },
  mounted:function() {
    $.getJSON("code_table.json").then((res)=>{
      this.codes = res;
      console.log("code read sucessly");
    });
    $.getJSON("courses.json").then((res)=>{
      this.courses = res
      console.log("courses read sucessly");
    });
    console.log(this.query_transalte['課程名稱']);
  },
  methods:{
    change_faculty_state(id){

      this.department='0';
      this.faculty = id;

      let $opt = $('.opt');

      this.remove_class($opt);

      $opt = $($opt.get(id));
      $opt.addClass('highlight');
    },
    change_department_state(id){
      this.department = this.codes[id];
      let $opt = $('.departments .opt');;
      this.remove_class($opt);

      $opt = $(`.opt:contains(${id})`);

      $opt.each((i,o)=>{
        console.log(o.innerText);
        if(o.innerText==id){
          $(o).addClass('highlight');
        }
      });

    },
    remove_class(target){
      Array.from(target).forEach((i)=>{
        // console.log(i);
        $(i).removeClass('highlight');
      });
    },

  },
  computed:{
    filter_courses:function () {
      let results=[];
      this.departments=[];
      const query_item = this.query_transalte[this.selected];
      // console.log(query_item);
      for(department in this.courses){
        if((!(department.match(new RegExp('^[a-z]','i'))&&this.faculty=='8'))&&(this.faculty!=department[0])&&this.faculty!='0') continue;
        if(this.faculty!='0'){
          this.departments.push(this.codes[department]);
        }
        if(department!=this.department&&this.department!='0') continue;

        this.courses[department].forEach((course)=>{
          const flag = course[query_item].toLowerCase().indexOf(this.filter.toLowerCase());
          if(flag!=-1){
            course['department'] = this.codes[department];
            results.push(course);
          }
        });
      }
      return results;
    },
  }
});
