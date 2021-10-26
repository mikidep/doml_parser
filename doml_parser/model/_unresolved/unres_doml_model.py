from .unres_model import UnresModel
from . import unres_metadata as um
from .unres_node_template import UnresNodeTemplate
from .unres_property_def import UnresPropertyDef
from .unres_output import UnresOutput

from ..doml_model import DOMLModel
from . import resolver as r


class UnresDOMLModel(UnresModel):
    def __init__(self, doml_dict: dict) -> None:
        super().__init__(doml_dict.get("imports", []))
        self.metadata: um.UnresMetadata \
            = um.UnresMetadata(doml_dict["metadata"])
        self.input: dict[str, UnresPropertyDef] \
            = {iname: UnresPropertyDef(iname, idict)
               for iname, idict in doml_dict.get("input", {}).items()}
        self.node_templates: dict[str, UnresNodeTemplate] \
            = {ntname: UnresNodeTemplate(ntname, ntdict)
               for ntname, ntdict
               in doml_dict.get("node_templates", {}).items()}
        self.output: dict[str, UnresOutput] \
            = {oname: UnresOutput(oname, odict)
               for oname, odict in doml_dict.get("output", {}).items()}

    def resolve(self, resolver: 'r.Resolver', ctx: 'r.ResolverCtx') \
            -> DOMLModel:
        metadata = self.metadata.resolve(resolver, ctx)
        input = {iname: i.resolve(resolver, ctx)
                 for iname, i in self.input.items()}
        ntctx = r.ResolverCtx(ctx.unres_model,
                              # ctx.node_type,
                              r.NodeTplCtx(self.node_templates, {}))
        node_templates = {ntname: nt.resolve(resolver, ntctx)
                          for ntname, nt in self.node_templates.items()}
        output = {oname: o.resolve(resolver, ntctx)
                  for oname, o in self.output.items()}
        return DOMLModel(metadata,
                         input,
                         node_templates,
                         output)
